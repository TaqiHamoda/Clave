import {
  Box,
  VStack,
  Grid,
  Text,
} from "@chakra-ui/react"

import { ColorModeSwitcher } from "../components/ColorModeSwitcher"
import { Logo } from "../components/Logo"

export const NotFoundPage = () => (
  <Box textAlign="center" fontSize="xl">
    <Grid minH="100vh" p={3}>
      <ColorModeSwitcher justifySelf="flex-end" />
      <VStack spacing={8}>
        <Logo h="40vmin" pointerEvents="none" />
        <Text fontSize='2xl' fontWeight='extrabold'> 404 Page Not Found </Text>
      </VStack>
    </Grid>
  </Box>
)
