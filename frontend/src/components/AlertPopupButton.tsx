import {
    Button,
    ButtonProps,
    useDisclosure,
    AlertDialog,
    AlertDialogOverlay,
    AlertDialogContent,
    AlertDialogHeader,
    AlertDialogBody,
    AlertDialogFooter,
} from "@chakra-ui/react"  
import { useRef } from "react";


export interface AlertPopupButtonProps extends Omit<ButtonProps, 'onClick'>{
    text: string,
    header: string,
    body: string,
    onClick: React.MouseEventHandler<HTMLButtonElement>
}

export const AlertPopupButton = (props: AlertPopupButtonProps) => {
    const {text, header, body, onClick, ...rest} = props;

    const { isOpen, onOpen, onClose } = useDisclosure();
    const cancelRef = useRef<any>();
  
    return <>
        <Button {...rest} onClick={onOpen}/>

        <AlertDialog
          isOpen={isOpen}
          leastDestructiveRef={cancelRef}
          onClose={onClose}
        >
          <AlertDialogOverlay>
            <AlertDialogContent>
              <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                {header}
              </AlertDialogHeader>
  
              <AlertDialogBody>
                {body}
              </AlertDialogBody>
  
              <AlertDialogFooter>
                <Button ref={cancelRef} onClick={onClose}>
                  Cancel
                </Button>
                <Button colorScheme={rest.colorScheme} onClick={e => {onClose(); onClick(e);}} ml={3}>
                  {text}
                </Button>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialogOverlay>
        </AlertDialog>
      </>;
  }