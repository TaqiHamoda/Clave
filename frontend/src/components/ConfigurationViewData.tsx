import {
    Text,
    HStack,
    Icon,
    SimpleGrid,
    Tag,
    Tooltip,
    useColorModeValue
} from "@chakra-ui/react"
import React from 'react';
import { CheckCircle, XCircle } from "react-bootstrap-icons";

import { ConfigProperty } from '../models/Configuration';

interface ConfigurationViewDataProps {
    name: string;
    value: any;
    config: ConfigProperty;
}

function ConvertConfigValue(configType: string, configUnit: string, value: any): React.ReactElement{
    switch (configType) {
        case 'number':
            value = (value as Number).toFixed(2);
            return <Text>
                {value} {configUnit}
            </Text>;
        case 'integer':
        case 'text':
        case 'enumeration':
            return <Text>
                {value} {configUnit}
            </Text>;
        case 'boolean':
            if (value as boolean) {
                return <HStack>
                    <Icon as={CheckCircle} color='green' fontSize='xl' />

                    <Text> True </Text>
                </HStack>;
            }

            return <HStack>
                    <Icon as={XCircle} color='red' fontSize='xl' />

                    <Text> False </Text>
                </HStack>;
        default:
            return <></>;
    }
}

export const ConfigurationViewData = ({ name, value, config }: ConfigurationViewDataProps) => {
    const background = useColorModeValue('blackAlpha.100', 'whiteAlpha.100');

    if (name == '_index') {
        return <div />;
    }

    var view: React.ReactNode;

    switch (config.type) {
        case 'list':
            view = <SimpleGrid  columns={[1, 2]} spacing='5px'>
                {(value as Array<any>).map(v => <Tag >
                    {ConvertConfigValue(config.value as string, config.unit as string, v)}
                </Tag>)}
            </SimpleGrid>;
            break;
        default:
            view = ConvertConfigValue(config.type, config.unit as string, value);
            break;
    }

    return <Tooltip label={config.description}>
        <HStack borderWidth='1px' borderRadius='lg' padding='10px' background={background} >
        <Text fontWeight='bolder'>
            {name}:
        </Text>

        {view}
    </HStack>
    </Tooltip>;
}