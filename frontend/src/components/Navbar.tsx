import {
    VStack,
    Button,
    IconButton,
    Spacer,
    Image,
    Center,
    Flex,
} from "@chakra-ui/react";
import { InfoCircle, JournalRichtext, GearFill } from "react-bootstrap-icons";
import { useNavigate, useLocation } from "react-router";

import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { NavbarLink } from "./NavbarLink";
import { ProfileButton } from "./ProfileButton";

import OpenCR_Logo from "../static/Open-CR-Logo.svg";

import { ENV } from '../services/Environment';

export const Navbar = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const navigateToPath = (e: any, path: string) => {
        e.preventDefault();

        navigate(path, {
            replace: false,
            state: {
                from: location
            },
        });
    }

    return <Flex padding='10px' direction='column'>
        <Button variant='link' onClick={(e) => navigateToPath(e, ENV.HOME_PATH)}>
            <Image src={OpenCR_Logo} height='75px' />
        </Button>

        <Spacer />

        <VStack spacing='20px'>
            <NavbarLink to={ENV.REPORTS_PATH} label='Go to Reports' icon={<JournalRichtext/>} />
            <NavbarLink to={ENV.SETTINGS_PATH} label='Go to Settings' icon={<GearFill/>} />
        </VStack>

        <Spacer />

        <Center>
            <ColorModeSwitcher marginRight='5px' />
            <IconButton
                marginLeft='5px'
                aria-label='About Open-CR'
                icon={<InfoCircle />}
                title='About Open-CR'
                onClick={(e) => navigateToPath(e, ENV.ABOUT_PATH)}
                size="md"
                fontSize="xl"
                variant="ghost"
                color="current" />
        </Center>
    </Flex>;
};
