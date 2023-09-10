import {
    Box,
    BoxProps,
    VStack,
    HStack,
    FormLabel,
    Progress,
    Text,
    IconButton,
    Flex
} from "@chakra-ui/react"  
import { useEffect, useState } from "react";

import { ArrowClockwise } from "react-bootstrap-icons";

import { ServerStats } from "../../models/ServerInfo";
import { ServerService } from "../../services/ServerService";

export const ServerResources = (props: BoxProps) => {
    const [serverStats, setServerStats] = useState<ServerStats | null>(null);
    const [serverMemoryStorageUsed, setServerMemoryStorageUsed] = useState<[number, number]>([0, 0]);

    const refresh = () => {
        ServerService.getResources().then(resources => {
            setServerStats(resources);

            if(resources != null){
                setServerMemoryStorageUsed([
                    resources.memory_total - resources.memory_free,
                    resources.disk_total - resources.disk_free
                ]);
            }
        });
    };

    useEffect(() => {
        refresh();
    }, []);

    return <Box {...props}>
        <Flex flexDirection='row-reverse'>
            <IconButton aria-label='Refresh Server Stats'
            title='Refresh Server Stats'
            icon={<ArrowClockwise/>}
            colorScheme='green'
            onClick={refresh} />
        </Flex>

        <VStack >
            <VStack alignItems='unset' width='full'>
                <FormLabel> CPU Percentage </FormLabel>
                <HStack alignItems='center' textAlign='right'>
                    <Progress value={serverStats?.cpu_percent}
                    min={0}
                    max={100}
                    size='xs'
                    colorScheme='blue'
                    isIndeterminate={serverStats == null}
                    width='full'/>
                    <Text maxWidth='100px' width='full'>
                        {serverStats == null ? '' : `${serverStats.cpu_percent}%`}
                    </Text>
                </HStack>
            </VStack>

            <VStack alignItems='unset' width='full'>
                <FormLabel> Memory Usage </FormLabel>
                <HStack alignItems='center' textAlign='right'>
                    <Progress value={serverMemoryStorageUsed[0]}
                    min={0}
                    max={serverStats?.memory_total}
                    size='xs'
                    colorScheme='blue'
                    isIndeterminate={serverStats == null}
                    width='full'/>
                    <Text maxWidth='100px' width='full'>
                        {serverStats == null ? '' : `${(serverMemoryStorageUsed[0] / 1024**3).toFixed(2)} GB`}
                    </Text>
                </HStack>
            </VStack>

            <VStack alignItems='unset' width='full'>
                <FormLabel> Disk Storage Usage </FormLabel>
                <HStack alignItems='center' textAlign='right'>
                    <Progress value={serverMemoryStorageUsed[1]}
                    min={0}
                    max={serverStats?.disk_total}
                    size='xs'
                    colorScheme='blue'
                    isIndeterminate={serverStats == null}
                    width='full'/>
                    <Text maxWidth='100px' width='full'>
                        {serverStats == null ? '' : `${(serverMemoryStorageUsed[1] / 1024**3).toFixed(2)} GB`}
                    </Text>
                </HStack>
            </VStack>
        </VStack>
    </Box>;
}
