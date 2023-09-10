import {
    Box,
    BoxProps,
    Flex,
    Text,
    SimpleGrid,
    VStack,
  } from "@chakra-ui/react";

import { ConfigurationViewData } from "../../components/ConfigurationViewData";

import { State } from "../../models/State";
import { Configuration } from "../../models/Configuration";

export interface StateInterfaceProps extends BoxProps{
    config?: Configuration,
    state?: State
}

export const StateInterface = (props: StateInterfaceProps) => {
    const {state, config, ...rest} = props;

    if (state == null || config == null) {
        return <></>;
    }

    return <Box {...rest}>
        <SimpleGrid columns={[1, 2]} gap='20px' marginTop='10px'>
            {Object.keys(config.state).map(key => {
                return <VStack borderRadius='md' borderWidth='1px'>
                    <Flex flexDirection='row' width='full' padding='10px'>
                        <Text fontSize='lg'> {key} </Text>
                    </Flex>

                    <SimpleGrid columns={[1, 2]} gap='10px' width='full' padding='5px'>
                        {Object.keys(config.state[key]).map(k => {
                            return <ConfigurationViewData name={k} value={state.state[key][k]} config={config.state[key][k]}/>;
                        })}
                    </SimpleGrid>
                </VStack>;
            })}
        </SimpleGrid>
    </Box>;
}