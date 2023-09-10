import {
  ColorModeScript,
  ChakraProvider,
} from "@chakra-ui/react"
import * as React from "react"
import { createRoot } from 'react-dom/client';
import { Router } from "./Router"

const root = createRoot(document.getElementById("root") as HTMLElement);

root.render(
  <React.StrictMode>
    <ColorModeScript />
    <ChakraProvider>
      <Router />
    </ChakraProvider>
  </React.StrictMode>
)
