import {
    Text,
    Image,
    HStack,
    VStack,
    Skeleton,
    Icon,
    Button,
    IconButton,
} from "@chakra-ui/react";
import { useState, useEffect } from 'react';
import { CheckCircle, ExclamationCircle, XCircle, Joystick, ArrowRepeat } from 'react-bootstrap-icons';
import { useLocation, useNavigate } from "react-router";

import { Module } from "../../models/Module";
import { Device } from "../../models/Device";
import { Commands } from "../../models/Commands";

import { CommandsService } from "../../services/CommandsService";
import { ModuleService } from "../../services/ModuleService";
import { DeviceService } from "../../services/DeviceService";
import { ENV } from "../../services/Environment";

import Open_CR_Logo from '../../static/Open-CR-Logo.svg';
import { ClickableCard } from '../ClickableCard';

interface DevicePanelProps {
    module: Module;
}

enum Status {
    ready = 0,
    running = 1,
    issue = 2
}

function getStatus(device: Device): Status {
    if (device.status?.issue) {
        return Status.issue;
    } else if (device.status?.running) {
        return Status.running;
    } else if (device.status?.ready) {
        return Status.ready;
    }

    return Status.issue;
}

function getMessage(device: Device): string {
    if (device.status == null) {
        return ''
    }

    if (device.status.error.length > 0) {
        return device.status.error;
    } else if (device.status.warning.length > 0) {
        return device.status.warning;
    } else if (device.status.info.length > 0) {
        return device.status.info;
    }

    return '';
}

export const DevicePanel = ({ module }: DevicePanelProps) => {
    const statusMap: Map<Status, any[]> = new Map([
        [Status.ready, ['blue.200', CheckCircle]],
        [Status.running, ['yellow.400', ExclamationCircle]],
        [Status.issue, ['red.400', XCircle]]
    ]);

    const [image, setImage] = useState<string>('');
    const [device, setDevice] = useState<Device | null>(null);
    const [updated, setUpdated] = useState<boolean>(false);
    const [loaded, setLoaded] = useState<boolean>(false);

    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {    
        ModuleService.getImage(module.name).then(image => {
            if (image != null) {
                setImage(`data:image/png;base64,${image.image}`);
            }

            setLoaded(true);
        });

        DeviceService.getDevice(module.name).then(reqDevice => {
            if ((reqDevice == null) || (reqDevice.status == null)) {
                return;
            }

            setDevice(reqDevice);
            setUpdated(true);
        });
    }, []);


    const onClickExperiment = (e: any) => {
        e.preventDefault();

        navigate(`${ENV.EXPERIMENT_PATH}/${encodeURIComponent(module.name)}`, {
            replace: false,
            state: {
                from: location
            },
        });
    };

    const refreshModule = (e: any) => {
        e.preventDefault();
        setUpdated(false);

        CommandsService.runCommand(module.name, Commands.getStatus, {}).then(result => {
            var error: string;

            if (typeof result === 'string') {
                error = result;
            } else if (!result.success) {
                error = result.error;
            } else {
                setTimeout(() => {
                    DeviceService.getDevice(module.name).then(reqDevice => {
                        if ((reqDevice == null) || (reqDevice.status == null)) {
                            return;
                        }

                        setDevice(reqDevice);
                        setUpdated(true);
                    });
                }, ENV.STATUS_REFRESH_TIMEOUT);
                return;
            }

            setUpdated(true);
            setDevice({
                name: module.name,
                status: {
                    carriages_count: 0,
                    info: '',
                    warning: '',
                    error: `Failed to refresh: ${error}`,
                    ready: false,
                    running: false,
                    issue: true,
                }
            });
        });
    }

    const buttons = (
        <HStack spacing='10px'>
            <Button
                title={`Create Experiment for ${module.name}`}
                onClick={onClickExperiment}
                leftIcon={<Icon fontSize='2xl' as={Joystick} />}>
                Create Experiment
            </Button>

            <IconButton
                colorScheme='blue'
                title='Refresh Interface Info'
                aria-label='Refresh Interface Info'
                size='md'
                onClick={refreshModule}
                isLoading={!updated}
                icon={<ArrowRepeat />} />
        </HStack>
    );

    return <Skeleton isLoaded={loaded} borderRadius='10px'>
        <ClickableCard
            to={`${ENV.MODULE_PATH}/${encodeURIComponent(module.name)}`}
            borderRadius='2xl'
            width='sm'
            child={buttons}
            padding='10px'
            title={`Go to the ${module.name} interface`}>
            <VStack spacing='20px'>
                <Image
                    src={image}
                    fallbackSrc={Open_CR_Logo}
                    alt={module.name}
                    width='500px'
                    height='200px'
                    borderRadius='20px' />

                <VStack spacing='10px'>
                    <Text
                        fontFamily='mono'
                        fontWeight='semibold'
                        fontSize='xl'
                        as='h4'
                        noOfLines={1}>
                        {module.name}
                    </Text>

                    <HStack alignItems='center'>
                        <Icon
                            as={(statusMap.get(device == null ? Status.issue : getStatus(device)) as any)[1]}
                            fontSize='2xl'
                            color={(statusMap.get(device == null ? Status.issue : getStatus(device)) as any)[0]} />

                        <Text
                            color={(statusMap.get(device == null ? Status.issue : getStatus(device)) as any)[0]}
                            fontFamily='monospace'
                            fontWeight='hairline'
                            fontSize='md'
                            noOfLines={[1, 2, 3, 4]}>
                            {device == null ? '' : getMessage(device)}
                        </Text>
                    </HStack>
                </VStack>
            </VStack>
        </ClickableCard>
    </Skeleton>;
}