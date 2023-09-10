import {
    Flex,
    FlexProps
} from "@chakra-ui/react";

export const Sidebar: React.FC<Omit<FlexProps, 'direction' | 'overflow'>> = (props) => (
    <Flex overflow='scroll' direction='column' {...props}/>
)
