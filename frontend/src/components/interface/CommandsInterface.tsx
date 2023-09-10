import {
    Box,
    BoxProps,
    Flex,
    Text,
    SimpleGrid,
    VStack,
    HStack,
    Spacer,
    Button,
    useToast
  } from "@chakra-ui/react";
import { useEffect, useState } from "react";

import { ConfigurationFormData } from "../../components/ConfigurationFormData";

import { Commands } from "../../models/Commands";
import { Configuration } from "../../models/Configuration";

import { CommandsService } from "../../services/CommandsService";

export interface CommandsInterfaceProps extends BoxProps{
    config?: Configuration,
}

export const CommandsInterface = (props: CommandsInterfaceProps) => {
    const {config,  ...rest} = props;
    const toast = useToast();
    
    if (config == null) {
        return <></>;
    }

    const onSubmit = (e: any, command: string) => {
        e.preventDefault();

        const parameters: Record<string, Record<string, any>> = {};
        parameters[command] = {};

        for(var [k, v] of Object.entries(config.commands[command])){
            var i = document.getElementById(`commands_${command}_${k}`) as any;
            parameters[command][k] = i.value;
        }

        CommandsService.runCommand(config.name, Commands.execute, {"parameters": parameters, "command": command}).then(result => {
            var error: string;

            if (typeof result === 'string') {
                error = result;
            } else if (!result.success) {
                error = result.error;
            } else {
                toast({
                    title: 'Executed Command Successfully',
                    description: `Executed the ${command} command successfully.`,
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
    }

    return <Box {...rest}>
        <SimpleGrid columns={[1]} gap='20px' marginTop='10px'>
            {Object.keys(config.commands).map(key => {
                return <form onSubmit={e => onSubmit(e, key)}>
                    <VStack borderRadius='md' borderWidth='1px' padding='10px'>
                        <Flex flexDirection='row' width='full' padding='10px'>
                            <Text fontSize='lg'> {key} </Text>
                            <Spacer/>
                            <Button colorScheme='blue' variant='outline' title={key} aria-label={key} type='submit'>
                                {key}
                            </Button>
                        </Flex>

                        <SimpleGrid columns={[1, 2, 3]} spacing='40px' width='full'>
                            {Object.keys(config.commands[key]).map(k => {
                                return <ConfigurationFormData name={k} id={`commands_${key}_${k}`} config={config.commands[key][k]}/>;
                            })}
                        </SimpleGrid>
                    </VStack>
                </form>;
            })}
        </SimpleGrid>
    </Box>;
}