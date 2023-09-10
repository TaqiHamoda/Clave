import {
    FormHelperText,
    FormControl,
    FormLabel,
    Input,
    InputGroup,
    InputLeftAddon,
    Switch,
    NumberInput,
    NumberInputField,
    NumberInputStepper,
    NumberIncrementStepper,
    NumberDecrementStepper,
    Select
} from "@chakra-ui/react"
import React from 'react';

import { ConfigProperty } from '../models/Configuration';

export interface ConfigurationFormDataProps {
    name: string;
    id: string;
    config: ConfigProperty;
}

interface CustomNumberInputProps{
    id: string;
    min?: number | undefined;
    max?: number | undefined;
    unit?: string | undefined;
    step?: number | undefined;
}

const CustomNumberInput = ({ id, min, max, unit, step }: CustomNumberInputProps) => (
    <NumberInput id={id} min={min} max={max} step={step} placeholder={unit}>
        <InputGroup>
            <InputLeftAddon hidden={unit == null} children={unit}/>
            <NumberInputField />
        </InputGroup>
        <NumberInputStepper>
            <NumberIncrementStepper />
            <NumberDecrementStepper />
        </NumberInputStepper>
    </NumberInput>
);

export const ConfigurationFormData = ({ name, id, config }: ConfigurationFormDataProps) => {

    if (name == '_index') {
        return <div />;
    }

    var input: React.ReactNode;

    switch (config.type) {
        case 'text':
            input = <Input id={id} type='text' />;
            break;
        case 'number':
        case 'integer':
            input = (<CustomNumberInput
                id={id}
                min={config.min != null ? config.min : undefined}
                max={config.max != null ? config.max : undefined}
                unit={config.unit != null ? config.unit : undefined}
                step={config.step != null ? config.step : undefined}/>);
            break;
        case 'enumeration':
            input = (
                <Select variant='filled' id={id} >
                    {config.values != null ? config.values.map(value => <option value={value}>{value}</option>) : ''}
                </Select>
            );
            break;
        case 'boolean':
            input = <Switch id={id} />;
            break;
        default:
            console.error(`${config.type} is unsupported as a Form Type.`)
            input = '';
            break;
    }

    return <FormControl isRequired={config.type != 'boolean'} >
        <FormLabel htmlFor='text'>{name}</FormLabel>
        {input}
        <FormHelperText> {config.description} </FormHelperText>
    </FormControl>;
}