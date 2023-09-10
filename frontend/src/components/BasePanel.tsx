import {
    Text,
    Center,
    SimpleGrid,
    SimpleGridProps,
    Box,
  } from "@chakra-ui/react"

export const BasePanel = (props: SimpleGridProps) => {
    return <Box borderWidth='1px' borderRadius='lg' padding='25px' maxWidth='1200px' width='full'>
        <Center marginBottom='30px'>
            <Text fontSize='2xl' fontFamily='monospace'>
                Base Properties
            </Text>
        </Center>

        <SimpleGrid  {...props}/>
    </Box>;
}