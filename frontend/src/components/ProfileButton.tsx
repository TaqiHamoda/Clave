import {
    Button,
    ButtonProps,
    Avatar,
    Image,
    ImageProps
} from "@chakra-ui/react";

import { useState, useEffect } from "react";
import { AuthService } from "../services/AuthService";

import { User } from '../models/User';
import * as ImageModel from "../models/Image";
import OpenCR_Icon from "../static/Open-CR-Icon.svg";

interface ProfileButtonProps extends Omit<Omit<Omit<Omit<ImageProps, 'borderRadius'>, 'src'>, 'alt'>, 'onClick'>
{
    onClick?: React.MouseEventHandler<HTMLButtonElement> | undefined
}

export const ProfileButton = (props: ProfileButtonProps) => {
    const { onClick, boxSize, ...rest } = props;

    // TODO: Get image from DB
    const [user, setUser] = useState<User | null>(null);
    const [image, setImage] = useState<ImageModel.Image>({ image: OpenCR_Icon, name: 'Open-CR Icon' });

    useEffect(() => {
        AuthService.getLoggedInUser().then(result => {
            if (result != null) {
                setUser(result);
            }
        });
    }, [])

    return <Button
        borderRadius='full'
        boxSize='fit-content'
        onClick={onClick}>
        <Image
            {...rest}
            borderRadius='full'
            boxSize={boxSize}
            src={image.image}
            alt={user != null ? `${user.first_name} ${user.last_name}` : ''}
        />
    </Button>;
}