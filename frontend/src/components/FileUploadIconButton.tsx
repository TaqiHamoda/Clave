import {
    Box,
    IconButton,
    IconButtonProps,
} from "@chakra-ui/react";

import { createRef } from "react";

export interface FileUploadIconButtonProps extends Omit<IconButtonProps, 'onClick'> {
    onClick: (files: FileList | null | undefined) => void;
    multiple?: boolean;
    accept?: string;
}

export const FileUploadIconButton: React.FC<FileUploadIconButtonProps> = (props) => {
    const { onClick, multiple, accept, ...rest } = props;

    const inputRef = createRef<HTMLInputElement>();

    const handleClick = (e: any) => {
        e.preventDefault();
        inputRef.current?.click();
    }

    return <Box>
        <IconButton onClick={e => handleClick(e)} {...rest} />
        <input
            type='file'
            multiple={multiple}
            accept={accept}
            hidden
            ref={inputRef}
            onChange={e => onClick(inputRef.current?.files)}/>
    </Box>
    ;
}