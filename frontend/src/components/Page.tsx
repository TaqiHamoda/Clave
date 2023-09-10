import React from 'react';

import {
    Box,
    Flex,
    Divider,
} from "@chakra-ui/react";

import { Navbar } from "./Navbar";

interface PageProps {
    children: React.ReactNode;
}

export const Page = (props: PageProps) => {
    return <Flex height='100vh' width='100vw'>
        <Navbar />

        <Divider orientation='vertical' />

        <Box overflow='scroll' height='100vh' width='full'>
            {props.children}
        </Box>
    </Flex>;
}