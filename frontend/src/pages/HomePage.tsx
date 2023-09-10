import {
  Box,
  SimpleGrid,
  VStack,
  Flex,
  Spacer,
  useToast
} from "@chakra-ui/react"
import React from "react";
import {CloudUploadFill} from "react-bootstrap-icons";


import { Module } from "../models/Module";
import { Experiment } from "../models/Experiment";

import { ModuleService } from "../services/ModuleService";
import { AuthService } from "../services/AuthService";
import { ExperimentService } from "../services/ExperimentService";

import { Page } from "../components/Page"
import { DevicePanel } from "../components/home/DevicePanel"
import { StatusBar } from "../components/home/StatusBar"
import { FileUploadButton } from "../components/FileUploadButton";

export const HomePage = () => {
  const [devices, setDevices] = React.useState<Module[]>([]);
  const [experiments, setExperiments] = React.useState<Experiment[]>([]);
  const [name, setName] = React.useState<string>('');
  const [uploading, setUploading] = React.useState<boolean>(false);

  const toast = useToast();

  React.useEffect(() => {
    AuthService.getLoggedInUser().then(user => {
      if ((user != null) && (user.first_name != null)) {
        setName(user.first_name);
      }
    });

    ModuleService.getModules().then(result => {
      if (result != null) {
        setDevices(result);
      }
    });

    ExperimentService.getExperiments().then(result => {
      if(result != null) {
        setExperiments(result);
      }
    });
  }, []);

  return <Page>
    <Box fontSize='xl'>
      <VStack spacing='40px'>
        <StatusBar firstName={name} experimentsCount={experiments.length} modulesInstalled={devices.length} />

        <SimpleGrid
          columns={[1, 2, 3]}
          spacing='40px'
          padding='0px 25px 25px 25px'>
          {devices.map(device => <DevicePanel module={device} />)}
        </SimpleGrid>
      </VStack>
    </Box>
  </Page>;
}
