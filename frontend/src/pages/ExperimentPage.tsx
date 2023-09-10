import {
  Text,
  Center,
  SimpleGrid,
  Box,
  Skeleton,
  Button,
  VStack,
  FormControl,
  FormLabel,
  Input,
  useToast
} from "@chakra-ui/react"
import { useState, useEffect } from "react";

import { useParams } from "react-router"

import { Configuration, ConfigProperty, ReportExperimentBoard } from "../models/Configuration"
import { Status } from "../models/Device";
import { Experiment } from "../models/Experiment";
import { Commands } from "../models/Commands";

import { ConfigurationService } from "../services/ConfigurationService"
import { DeviceService } from "../services/DeviceService";
import { AuthService } from "../services/AuthService";
import { CommandsService } from "../services/CommandsService";

import { InfoPanel } from "../components/InfoPanel";
import { ConfigurationFormData } from "../components/ConfigurationFormData";
import { BasePanel } from "../components/BasePanel";
import { CarriagePanel } from "../components/CarriagePanel";
import { Page } from "../components/Page"


function getConfigPropertyValue(config: ConfigProperty, target: any): any {
  switch (config.type) {
    case 'boolean':
      return target.checked;
    case 'number':
      return Number.parseFloat(target.value);
    case 'integer':
      return Number.parseInt(target.value);
    case 'enumeration':
      return getConfigPropertyValue({ type: config.value as string, description: config.description }, target);
    default:
      return target.value;
  }
}

export const ExperimentPage = () => {
  const params = useParams();
  const toast = useToast();

  const [config, setConfig] = useState<Configuration | null>(null);
  const [carraiges, setCarriages] = useState<number[]>([]);
  const [submitted, setSubmitted] = useState<boolean>(true)

  useEffect(() => {
    if (params.moduleId == null) {
      return;
    }

    DeviceService.getDevice(params.moduleId as string).then(res => {
      if (res == null) {
        return;
      }

      const carr: number[] = []

      for (var c = 0; c < (res.status as Status).carriages_count; c++) {
        carr.push(c);
      }

      setCarriages(carr);

      ConfigurationService.getConfiguration(params.moduleId as string).then(result => {
        if (result != null) {
          setConfig(result);
        }
      });
    });
  }, [])

  const onSubmit = (e: any) => {
    e.preventDefault();
    setSubmitted(false);

    const parameters: ReportExperimentBoard = { base: {}, carriage: [] };

    for (var key of Object.keys(config?.experiment.base)) {
      parameters.base[key] = getConfigPropertyValue(config?.experiment.base[key], e.target[`base_${key}`]);
    }

    for (var c of carraiges) {
      var carr: Record<string, any> = {};
      for (key of Object.keys(config?.experiment.carriage)) {
        if (key == '_index') {
          carr._index = c;
          continue;
        }

        carr[key] = getConfigPropertyValue(config?.experiment.carriage[key], e.target[`carriage${c}_${key}`])
      }

      parameters.carriage.push(carr);
    }

    AuthService.getLoggedInUser().then(user => {
      if (user == null) {
        return;
      }

      const exp: Experiment = {
        name: e.target.experiment_name.value,
        user: user.username,
        timestamp: Date.now().toString(),
        module: params.moduleId as string,
        parameters: parameters,
      }

      CommandsService.runCommand(exp.module, Commands.run, exp).then(result => {
        setSubmitted(true);

        var error: string;

        if (typeof result === 'string') {
          error = result;
        } else if (!result.success) {
          error = result.error;
        } else {
          toast({
            title: 'Experiment Created Successfully',
            description: 'The experiment has been created successfully. The data should be found in the reports page.',
            status: 'info',
            duration: 9000,
            isClosable: true,
          });
          return;
        }

        toast({
          title: 'Issue Encountered',
          description: error,
          status: 'error',
          duration: 9000,
          isClosable: true,
        });
      });
    });
  };

  return <Page>
    <Center width='full'>
      <InfoPanel width='full'>
        <Text noOfLines={[1, 2, 3]} fontSize='4xl' fontFamily='monospace'>
          Create an Experiment for {params.moduleId == null ? '' : params.moduleId}
        </Text>
      </InfoPanel>
    </Center>

    <Skeleton isLoaded={config != null} borderRadius='25px' margin='25px'>

      <form onSubmit={onSubmit}>
        <VStack spacing='50px' marginTop='50px' >
          <Box borderWidth='1px' borderRadius='lg' padding='25px' maxWidth='1200px' width='full'>
            <Center marginBottom='30px'>
              <Text fontSize='2xl' fontFamily='monospace'>
                Experiment Properties
              </Text>
            </Center>


            <SimpleGrid columns={[1, 2, 3]} spacing='40px'>
              <FormControl isRequired>
                <FormLabel htmlFor='text'> Experiment Name </FormLabel>
                <Input id='experiment_name' type='text' />
              </FormControl>
            </SimpleGrid>
          </Box>

          <BasePanel columns={[1, 2, 3]} spacing='40px'>
            {config != null ? Object.keys(config.experiment.base).map((key: string) =>
              <ConfigurationFormData
                name={key}
                id={`base_${key}`}
                config={config.experiment.base[key] as ConfigProperty} />) : ''}
          </BasePanel>

          <CarriagePanel
            carriageConfig={config == null ? {} : config.experiment.carriage}
            columns={[1, 2, 3]}
            spacing='40px'/>

          <Button width='lg' type='submit' isLoading={!submitted} title='Create Experiment' aria-label='Create Experiment'>
            Create Experiment
          </Button>
        </VStack>
      </form>
    </Skeleton>
  </Page>;
}
