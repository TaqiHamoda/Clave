import {
    VStack,
    BoxProps,
} from "@chakra-ui/react";

export const InfoPanel = (props: BoxProps) => {
    const {
        borderRadius,
        border,
        borderColor,
        boxShadow,
        padding,
        maxWidth,
        marginTop,
        textAlign,
        ...rest
    } = props;


    return <VStack
    borderRadius='2xl'
    border='2px'
    borderColor='rgba(9, 118, 178, 0.20)'
    boxShadow='5px 5px 5px 5px rgba(9, 118, 178, 0.20)'
    padding='20px'
    maxWidth='900px'
    marginTop='20px'
    textAlign='center'
    {...rest}/>;
} 