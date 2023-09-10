import {
  Flex,
  Text,
  SimpleGrid,
  VStack,
  Skeleton,
  IconButton,
  useToast
} from "@chakra-ui/react";
import { CloudArrowDownFill } from "react-bootstrap-icons";
import { useParams } from "react-router";
import { useState, useEffect } from "react";

import { Page } from "../components/Page";
import { StateInterface } from "../components/interface/StateInterface";
import { SettingsInterface } from "../components/interface/SettingsInterface";
import { CommandsInterface } from "../components/interface/CommandsInterface";

import { State } from "../models/State";
import { Device } from "../models/Device";
import { Configuration } from "../models/Configuration";
import { ModuleService } from "../services/ModuleService";
import { StateService } from "../services/StateService";
import { DeviceService } from "../services/DeviceService";
import { ConfigurationService } from "../services/ConfigurationService";


interface InterfaceObjects{
  name: string,
  component: React.ReactElement
}


export const InterfacePage = () => {
  const params = useParams();
  const toast = useToast();

  const [config, setConfig] = useState<Configuration | null>(null);
  const [device, setDevice] = useState<Device | null>(null);
  const [state, setState] = useState<State | null>(null);

  const interfaceObjects: InterfaceObjects[] = [
    {
      name: "Interface State",
      component: <StateInterface config={config as Configuration} state={state as State} />
    },
    {
      name: "Interface Settings",
      component: <SettingsInterface config={config as Configuration} device={device as Device} />
    },
    {
      name: "Interface Commands",
      component: <CommandsInterface config={config as Configuration} />
    }
  ]

  useEffect(() => {
    if (params.moduleId == null) {
      return;
    }

    StateService.getState(params.moduleId).then(result => {
      if (result != null) {
        setState(result);
      } else {
        toast({
          title: 'Cannot load interface state data.',
          description: 'Cannot load the interface state data. Please check the logs for more info.',
          status: 'error',
          duration: 9000,
          isClosable: true,
        });
      }
    });

    DeviceService.getDevice(params.moduleId).then(result => {
      if (result != null) {
        setDevice(result);
      } else {
        toast({
          title: 'Cannot load settings data.',
          description: 'Cannot load the interface data. Please check the logs for more info.',
          status: 'error',
          duration: 9000,
          isClosable: true,
        });
      }
    });

    ConfigurationService.getConfiguration(params.moduleId).then(result => {
      if (result != null) {
        setConfig(result);
      } else {
        toast({
          title: 'Cannot load configuration data.',
          description: 'Cannot load the configuration data for this interface. Please check the logs for more info.',
          status: 'error',
          duration: 9000,
          isClosable: true,
        });
      }
    });
  }, []);

  return <Page>
    <Skeleton paddingTop='25px' height='full' isLoaded={config != null && device != null && state != null}>
      <Flex width='full' flexDirection='row-reverse' padding='20px'>
        <IconButton
        title='Export Interface'
        colorScheme='blue'
        variant='outline'
        icon={<CloudArrowDownFill />}
        size='lg'
        fontSize='2xl'
        aria-label='Export Interface'
        onClick={e => { e.preventDefault(); ModuleService.downloadInterface(params.moduleId as string); }}/>
      </Flex>

      <SimpleGrid columns={[1]} spacing='30px' padding='20px'>
        {interfaceObjects.map(o => <VStack alignItems='unset'>
          <Flex width='full'>
            <Text fontFamily='monospace' fontSize='xl' fontWeight='medium'>
              {o.name}
            </Text>  
          </Flex>

          {o.component}
        </VStack>)}
      </SimpleGrid>
    </Skeleton>
  </Page>;
}
