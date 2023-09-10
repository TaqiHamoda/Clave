import {
  Box,
  Text,
  Link,
  VStack,
  Image,
  Icon
} from "@chakra-ui/react"
import Logo from "../static/Open-CR-Logo.svg";

import { BoxArrowUpRight } from 'react-bootstrap-icons';
import { Page } from "../components/Page";

export const AboutPage = () => (
  <Page>
    <Box textAlign="center" fontSize="xl">
      <VStack spacing='100px' marginTop='100px'>
        <Image src={Logo} h="40vmin" pointerEvents="none" />

        <VStack maxWidth='1000px' spacing='25px'>
          <Text
          noOfLines={[3, 4, 5]}
          fontFamily='monospace'
          fontSize='2xl'
          fontWeight='semibold'>
            Open-CR is a Robot Management Platform that was developed in the Continuum Robotics Lab at the University of Toronto Mississauga.
          </Text>

          <Text
          noOfLines={[3, 4, 5]}
          fontFamily='monospace'
          fontSize='2xl'
          fontWeight='semibold'>
            Our goal is accessibility. Open-CR was created with the goal of making Robotic research accessible to a wider audience (and hopefully everyone).
          </Text>
          
          <Link href='https://crl.utm.utoronto.ca' isExternal>
            Continuum Robotics Lab <Icon as={BoxArrowUpRight}/>
          </Link>
        </VStack>
      </VStack>
    </Box>
  </Page>
)
