import {
    Center,
    LinkOverlay,
    LinkBox,
    LinkBoxProps,
    useColorModeValue,
} from "@chakra-ui/react";

import { ReactNode } from "react";

import { useNavigate, useLocation } from "react-router";

export interface ClickableCardProps extends Omit<LinkBoxProps, 'background'> {
    to: string;
    child?: ReactNode;
}

export const ClickableCard: React.FC<ClickableCardProps> = (props) => {
    const { to, child, children, ...rest } = props;
    const background = useColorModeValue('blackAlpha.100', 'whiteAlpha.100');
    const backgroundHover = useColorModeValue('gray.200', 'gray.700');

    const navigate = useNavigate();
    const location = useLocation();

    const onClick = (e: any) => {
        e.preventDefault();

        navigate(to, {
            replace: false,
            state: {
                from: location
            },
        });
    }

    return <LinkBox
        background={background}
        _hover={{ background: backgroundHover, cursor: 'pointer' }}
        transition='background 0.2s'
        {...rest}>
        <LinkOverlay onClick={onClick}>
            {children}
        </LinkOverlay>

        <Center marginTop='10px'>
            {child}
        </Center>
    </LinkBox>;
}