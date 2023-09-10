import {
    SimpleGrid,
    Divider,
    Text,
} from "@chakra-ui/react";
import { Controller, Plugin, HeartFill } from 'react-bootstrap-icons';

import { InfoPanel } from "../InfoPanel";
import { Status } from './Status';

interface StatusBarProps {
    firstName: string;
    modulesInstalled: number;
    experimentsCount: number;
    funFact?: string;
}

export const StatusBar = ({ firstName, modulesInstalled, experimentsCount, funFact }: StatusBarProps) => {
    return <InfoPanel>
        <Text fontSize='4xl' fontFamily='monospace'>
            Welcome Back{firstName.length > 0 ? `, ${firstName}!` : '!'}
        </Text>

        <Divider />

        <SimpleGrid columns={[1, 2, 3]} paddingTop='20px' width='full' spacing='15px'>
            <Status
                text={`${experimentsCount} Experiments Executed`}
                icon={Controller} />

            <Status
                text={`${modulesInstalled} Interfaces Installed`}
                icon={Plugin} />

            <Status
                text={`${Math.floor(0.61 * experimentsCount)} Prototypes Saved`}
                icon={HeartFill} />
        </SimpleGrid>

        <Text
            fontFamily='monospace'
            fontSize='2xl'
            paddingTop='20px'
            noOfLines={[1, 2, 3]}>
            {funFact != null ? funFact : 'Fun Fact: Open-CR was fully developed by an awesome undergrad volunteer!'}
        </Text>
    </InfoPanel>;
};