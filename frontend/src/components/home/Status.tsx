import {
    Text,
    HStack,
    Center,
    Icon,
} from "@chakra-ui/react";

interface StatusProps {
    text: string;
    icon: any;
}

export const Status = ({ text, icon }: StatusProps) => {
    return <Center>
        <HStack>
            <Icon as={icon} color='blue.400' />
            <Text fontSize='xl'>
                {text}
            </Text>
        </HStack>
    </Center>
}