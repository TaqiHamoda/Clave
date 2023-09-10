import {
  Center,
  Skeleton,
  SimpleGrid,
  HStack,
  Button,
  Text,
  VStack,
  IconButton,
  Flex,
  Tabs,
  Tab,
  TabList,
  TabPanels,
  TabPanel,
  Spacer,
  Badge
} from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { CloudArrowDownFill } from 'react-bootstrap-icons';

import { Configuration } from '../models/Configuration';
import { Experiment } from '../models/Experiment';

import { ReportService } from '../services/ReportService';
import { ConfigurationService } from '../services/ConfigurationService';
import { ExperimentService } from '../services/ExperimentService';

import { LineChart } from '../components/LineChart';
import { Page } from '../components/Page';
import { InfoPanel } from "../components/InfoPanel";
import { ConfigurationViewData } from '../components/ConfigurationViewData';
import { BasePanel } from '../components/BasePanel';
import { CarriagePanel } from '../components/CarriagePanel';

interface ReportObject {
  label: string,
  unit: string,
  dataset: any[],
  type: string
}

export const ReportPage = () => {
  const params = useParams();

  const [experiment, setExperiment] = useState<Experiment | null>(null);
  const [configuration, setConfiguration] = useState<Configuration | null>(null);

  const [yObjects, setYObjects] = useState<Record<string, ReportObject>>({});

  const [yUnits, setYUnits] = useState<Record<string, string[]>>({});
  const [yInfo, setYInfo] = useState<string[]>([]);  // A list of property ids to be graphed and their colors
  const [yIndependent, setYIndependent] = useState<string[]>([]);

  const [xData, setXData] = useState<number[]>([]);
  const [xInfo, setXInfo] = useState<[string, string, number[]]>(['', '', []]);  // ID, Unit, Data

  useEffect(() => {
    ReportService.getReport(params.reportId as string).then(result => {
      if (result == null) {
        return;
      }

      ExperimentService.getExperiment(params.reportId as string).then(res => {
        if (res != null) {
          setExperiment(res);
        }
      });

      ConfigurationService.getConfiguration(result.module).then(res => {
        if (res == null) {
          return;
        }

        setConfiguration(res);

        ReportService.getReportData(result.experiment).then(data => {
          if (data == null) {
            return;
          }

          var index: string = '';
          var x_info: [string, string, number[]] = ['', 'milliseconds', []];

          var y_objects: Record<string, ReportObject> = {};
          
          var y_units: Record<string, string[]> = {};
          var y_independent: string[] = [];

          const earliest_time: number = Number(new Date(data.data[0][0]));  // Unix Epoch milliseconds
          for (var datapoint of data.data) {
            x_info[2].push((Number(new Date(datapoint[0])) - earliest_time));  // Normalize the time-axis

            for (var [key, value] of Object.entries(datapoint[1].base)) {
              index = `base_${key}`;
              if (y_objects[index] == null) {
                y_objects[index] = {
                  label: key,
                  unit: res.report.base[key].unit,
                  dataset: [value],
                  type: 'Base'
                };
                
                if (res.report.base[key].independent == true) {
                  y_independent.push(index);
                  y_objects[index].type = 'Independent';
                  continue;
                }

                if (y_units[res.report.base[key].unit] == null) { y_units[res.report.base[key].unit] = []; }
                y_units[res.report.base[key].unit].push(index);
              } else {
                y_objects[index].dataset.push(value);
              }
            }

            for (var carriage of datapoint[1].carriage) {
              for (var [key, value] of Object.entries(carriage)) {
                if (key == '_index') { continue; }

                index = `carriage${carriage['_index']}_${key}`;
                if (y_objects[index] == null) {
                  y_objects[index] = {
                    label: key,
                    unit: res.report.carriage[key].unit,
                    dataset: [value],
                    type: `Carriage ${Number.parseInt(carriage['_index']) + 1}`
                  };

                  if (res.report.carriage[key].independent == true) {
                    y_independent.push(index);
                    y_objects[index].type = 'Independent';
                    continue;
                  }
  
                  if (y_units[res.report.carriage[key].unit] == null) { y_units[res.report.carriage[key].unit] = []; }
                  y_units[res.report.carriage[key].unit].push(index);
                } else {
                  y_objects[index].dataset.push(value);
                }
              }
            }
          }

          setXData(x_info[2]);
          setXInfo(x_info);

          setYObjects(y_objects);

          setYUnits(y_units);
          setYIndependent(y_independent.filter((v, i, a) => a.indexOf(v) === i));
        });
      });
    });
  }, []);

  const onButtonClick = (e: any) => {
    e.preventDefault();

    if (xInfo[0] == e.currentTarget.id) {
      return
    }

    if (yInfo.includes(e.currentTarget.id)) {
      setYInfo(yInfo.filter((id => id != e.currentTarget.id)));
    } else {
      setYInfo([...yInfo, e.currentTarget.id]);
    }
  }

  const onButtonDoubleClick = (e: any) => {
    e.preventDefault();

    if (yInfo.includes(e.currentTarget.id)) {
      setYInfo(yInfo.filter((id => id != e.currentTarget.id)));
    }

    if (xInfo[0] == e.currentTarget.id) {
      setXInfo(['', 'milliseconds', xData]);
    } else {
      setXInfo([e.currentTarget.id, yObjects[e.currentTarget.id].unit, yObjects[e.currentTarget.id].dataset]);
    }
  }

  return <Page>
    <Center width='full'>
      <InfoPanel width='full'>
        <Text noOfLines={[1, 2, 3]} fontSize='4xl' fontFamily='monospace'>
          {params.reportId} Report
        </Text>
      </InfoPanel>
    </Center>

    <VStack spacing='25px' padding='25px'>
      <Flex direction='row-reverse' width='full'>
        <Skeleton isLoaded={xInfo[1].length > 0}>
          <IconButton
            aria-label='Export Experiment'
            title='Export Experiment'
            icon={<CloudArrowDownFill />}
            size='lg'
            fontSize='2xl'
            onClick={e => { e.preventDefault(); ReportService.downloadReport(params.reportId as string); }} />
        </Skeleton>
      </Flex>

      <Skeleton isLoaded={xInfo[1].length > 0} width='full'>
      <Tabs isFitted variant='enclosed'>
            <TabList marginBottom='1em'>
                {Object.keys(yUnits).map(unit => <Tab> {unit} </Tab>)}
            </TabList>

            <TabPanels>
                {Object.keys(yUnits).map(unit =>
                    <TabPanel>
                        <HStack >
                          <VStack
                            overflow='scroll'
                            padding='10px'
                            height='670px'
                            width='full'
                            maxWidth='400px'
                            textAlign='left'
                            borderWidth='1px'
                            borderRadius='lg'>
                            {[...yUnits[unit], ...yIndependent].map(key =>
                              <Button
                                id={key}
                                width='350px'
                                padding='25px'
                                colorScheme={xInfo[0] == key ? 'blue' : (yInfo.includes(key) ? 'green' : 'gray')}
                                onClick={onButtonClick}
                                onDoubleClick={onButtonDoubleClick}>
                                  <Flex width='full' alignItems='center'>
                                    <Text> {yObjects[key].label} </Text>
                                    <Spacer/>
                                    <Badge padding='2.5px'> {yObjects[key].type} </Badge>
                                  </Flex>
                              </Button>)}
                          </VStack>
                          <LineChart
                            width='full'
                            maxWidth='1300px'
                            borderWidth='1px'
                            borderRadius='lg'
                            padding='25px'
                            xLabel={xInfo[1]}
                            xData={xInfo[2]}
                            yLabel={unit}
                            yLabels={yInfo.filter(k => yUnits[unit].includes(k)).map(key => `${yObjects[key].label} - ${yObjects[key].type}`)}
                            yDatasets={yInfo.filter(k => yUnits[unit].includes(k)).map(key => yObjects[key].dataset)} />
                        </HStack>
                    </TabPanel>)}
            </TabPanels>
        </Tabs>
      </Skeleton>

      <SimpleGrid columns={[1, 2]} gap='25px' width='full'>
        <BasePanel columns={[1, 2]} spacing='40px'>
          {Object.keys(experiment == null ? {} : experiment.parameters.base).map(key => <ConfigurationViewData
            name={key}
            value={experiment?.parameters.base[key]}
            config={configuration?.experiment.base[key]} />)}
        </BasePanel>

        <CarriagePanel
          columns={[1, 2]}
          spacing='40px'
          carriageConfig={configuration == null ? {} : configuration.experiment.carriage}
          experiment={experiment as Experiment} />
      </SimpleGrid>
    </VStack>
  </Page>;
}