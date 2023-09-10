import {
    IconButton,
} from '@chakra-ui/react';
import {ReactElement} from 'react';


import { useNavigate, useLocation } from 'react-router-dom';

interface NavbarLinkProps {
    to: string;
    label: string;
    icon: ReactElement;
};

export const NavbarLink = ({ to, label, icon }: NavbarLinkProps) => {
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

    return <IconButton
    title={label}
    aria-label={label}
    size='lg'
    fontSize='2xl'
    icon={icon}
    onClick={onClick} />
}