import {
    Box,
    Button,
    ButtonProps,
} from "@chakra-ui/react";

import { createRef } from "react";

export interface FileUploadButtonProps extends Omit<ButtonProps, 'onClick'> {
    onClick: (files: FileList | null | undefined) => void;
    multiple?: boolean;
    accept?: string;
}

export const FileUploadButton: React.FC<FileUploadButtonProps> = (props) => {
    const { onClick, multiple, accept, ...rest } = props;

    const inputRef = createRef<HTMLInputElement>();

    const handleClick = (e: any) => {
        e.preventDefault();
        inputRef.current?.click();
    }

    return <Box>
        <Button onClick={handleClick} {...rest} />
        <input
            type='file'
            multiple={multiple}
            hidden
            accept={accept}
            ref={inputRef}
            onChange={e => onClick(inputRef.current?.files)}/>
    </Box>;
}