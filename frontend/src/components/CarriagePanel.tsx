import {
    Tab,
    Tabs,
    TabList,
    TabPanel,
    TabPanels,
    Text,
    Center,
    SimpleGrid,
    SimpleGridProps,
    Box,
} from "@chakra-ui/react"

import { ConfigurationFormData } from "./ConfigurationFormData";
import { ConfigurationViewData } from "./ConfigurationViewData";

import { Configuration, ConfigProperty } from "../models/Configuration";
import { Experiment } from "../models/Experiment";

export interface CarriagePanelProps extends SimpleGridProps {
    carriageConfig?: any,
    experiment?: Experiment
}

export const CarriagePanel = (props: CarriagePanelProps) => {
    const { carriageConfig, experiment, ...rest } = props;

    const carriageCount: number = Object.keys(carriageConfig).length;

    return <Box borderWidth='1px' borderRadius='lg' padding='25px' maxWidth='1200px' width='full' hidden={carriageCount == 0}>
        <Center marginBottom='30px'>
            <Text fontSize='2xl' fontFamily='monospace'>
                Carriage Properties
            </Text>
        </Center>

        <Tabs isFitted variant='enclosed'>
            <TabList marginBottom='1em'>
                {Array.from({ length: carriageCount }, (_, i) => i).map(c => <Tab> {`Carriage ${c + 1}`} </Tab>)}
            </TabList>

            <TabPanels>
                {Array.from({ length: carriageCount }, (_, i) => i).map(c =>
                    <TabPanel>
                        <SimpleGrid {...rest}>
                            {experiment == null ?

                            Object.keys(carriageConfig).map(key =>
                                <ConfigurationFormData
                                    name={key}
                                    id={`carriage${c}_${key}`}
                                    config={carriageConfig[key] as ConfigProperty} />) :

                            Object.keys(experiment?.parameters.carriage[c]).map(key => <ConfigurationViewData
                                name={key}
                                value={experiment?.parameters.carriage[c][key]}
                                config={carriageConfig[key]} />)}
                        </SimpleGrid>
                    </TabPanel>)}
            </TabPanels>
        </Tabs>
    </Box>;
}