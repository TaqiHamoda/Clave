import {
    Box,
    BoxProps,
    SimpleGrid,
    Input,
    IconButton,
    FormLabel,
    Select,
    HStack,
    VStack,
    Button,
    Center,
    Flex,
    Spacer,
    Text,
    Modal,
    ModalBody,
    ModalContent,
    ModalOverlay,
    ModalHeader,
    ModalCloseButton,
    ModalFooter,
    useDisclosure,
    useToast
} from "@chakra-ui/react"  
import { useEffect, useState } from "react";
import { TrashFill } from "react-bootstrap-icons";

import { AlertPopupButton } from "../AlertPopupButton";

import { User } from "../../models/User";
import { UserService } from "../../services/UserService";

export const AccountSettings = (props: BoxProps) => {
    const [users, setUsers] = useState<User[]>([]);

    useEffect(() => {
        UserService.getUsers().then(u => setUsers(u != null ? u : []));
    }, []);

    return <Box {...props}>
        <Flex flexDirection='row-reverse'>
            <NewUserModal/>
        </Flex>
        
        <SimpleGrid columns={[1, 2]} gap='20px' marginTop='10px'>
            {users.map(u => <UserSettingsCard user={u}/>)}
        </SimpleGrid>
    </Box>;
}

const UserSettingsCard = ( {user}: {user: User} ) => {
    const toast = useToast();

    useEffect(() => {
        var i = document.getElementById(`${user.username}-first_name`) as any;
        i.value = user.first_name;
        
        i = document.getElementById(`${user.username}-last_name`) as any;
        i.value = user.last_name;

        i = document.getElementById(`${user.username}-role`) as any;
        i.value = user.role;
    }, []);

    const updateUser = (e: any) => {
        e.preventDefault();
        
        const new_user: User = {
            username: user.username,
            first_name: (document.getElementById(`${user.username}-first_name`) as any).value,
            last_name: (document.getElementById(`${user.username}-last_name`) as any).value,
            role: Number((document.getElementById(`${user.username}-role`) as any).value),
        }

        UserService.updateUser(user.username, new_user).then(v => {
            if (v == true) {
                toast({
                    title: 'User Updated Successfully',
                    description: 'The user information has been updated successfully.',
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
            } else {
                toast({
                    title: 'Issue Encountered',
                    description: 'Could not update user. Please check the logs for more information.',
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                });
            }
        });
    };

    const changePassword = (e: any) => {
        e.preventDefault();
        
        const password: string = (document.getElementById(`${user.username}-password`) as any).value
        UserService.changePassword(user.username, password).then(v => {
            if (v == true) {
                toast({
                    title: "User's Password Updated Successfully",
                    description: "The user's password has been updated successfully.",
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
            } else {
                toast({
                    title: 'Issue Encountered',
                    description: "Could not update user's password. Please check the logs for more information.",
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                });
            }
        });
    };

    const deleteUser = (e: any) => {
        e.preventDefault();

        UserService.deleteUser(user.username).then(v => {
            if (v == true) {
                toast({
                    title: "User Removed Successfully",
                    description: "The user has been removed from the system successfully.",
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
            } else {
                toast({
                    title: 'Issue Encountered',
                    description: "Could not remove the user. Please check the logs for more information.",
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                });
            }
        });
    }

    return <Box borderWidth='1px' borderRadius='lg' padding='10px' width='fit-content'>
        <VStack gap='15px' alignItems='center'>
            <Flex flexDirection='row' width='full'>
                <Text>
                    {user.username}    
                </Text>
                <Spacer/>
                <AlertPopupButton
                    text='Delete User'
                    header='Delete User'
                    body="Are you sure? You can't undo this action afterwards."
                    aria-label='Delete User'
                    title='Delete User'
                    colorScheme='red'
                    onClick={deleteUser}>
                        <TrashFill />
                </AlertPopupButton>
            </Flex>

            <HStack gap='20px'>
                <VStack alignItems='unset'>
                    <FormLabel>First Name</FormLabel>
                    <Input id={`${user.username}-first_name`}/>
                </VStack>

                <VStack alignItems='unset'>
                    <FormLabel>Last Name</FormLabel>
                    <Input id={`${user.username}-last_name`}/>
                </VStack>

                <VStack alignItems='unset'>
                    <FormLabel>Role</FormLabel>
                    <Select variant="filled" id={`${user.username}-role`}>
                        <option value={0}>Admin</option>
                        <option value={1}>User</option>
                    </Select>
                </VStack>
            </HStack>
        
            <Button colorScheme='blue' size='md' maxWidth='500px' width='full' marginBottom='25px' onClick={updateUser}> Update User </Button>

            <VStack alignItems='unset' width='full'>
                <FormLabel>Password</FormLabel>
                <Input placeholder='New Password' id={`${user.username}-password`} type='password'/>
                
                <Center>
                    <AlertPopupButton
                        text='Change Password'
                        header='Change Password'
                        body="Are you sure you want to change the password?"
                        aria-label='Change Password'
                        title='Change Password'
                        colorScheme='red'
                        variant='outline'
                        maxWidth='200px'
                        width='full'
                        size='md'
                        onClick={changePassword}>
                            Change Password
                    </AlertPopupButton>
                </Center>
            </VStack>
        </VStack>
    </Box>;
}

const NewUserModal = () => {
    const { isOpen, onOpen, onClose } = useDisclosure()
    const toast = useToast();

    const createUser = (e: any) => {
        e.preventDefault();
        onClose();
        
        const new_user: User = {
            username: (document.getElementById('new_username') as any).value,
            first_name: (document.getElementById('new_first_name') as any).value,
            last_name: (document.getElementById('new_last_name') as any).value,
            role: Number((document.getElementById('new_role') as any).value),
            password: (document.getElementById('new_password') as any).value
        }

        UserService.createUser(new_user).then(v => {
            if (v == true) {
                toast({
                    title: 'User Created Successfully',
                    description: 'The user has been created successfully. Time for them to enjoy Open-CR ^_^',
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
            } else {
                toast({
                    title: 'Issue Encountered',
                    description: 'Could not create user. Please ensure that the username has not already been used.',
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                });
            }
        });
    };

    return <>
        <Button colorScheme='green' variant='outline' onClick={onOpen}>
            Create New User
        </Button>

        <Modal isOpen={isOpen} onClose={onClose}>
            <ModalOverlay />
            <ModalContent>
                <ModalHeader> Create a New User </ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <VStack gap='10px' alignItems='unset'>
                        <HStack gap='20px'>
                            <VStack alignItems='unset'>
                                <FormLabel>Username</FormLabel>
                                <Input id={'new_username'}/>
                            </VStack>

                            <VStack alignItems='unset'>
                                <FormLabel>Role</FormLabel>
                                <Select variant="filled" id={'new_role'}>
                                    <option value={0}>Admin</option>
                                    <option value={1}>User</option>
                                </Select>
                            </VStack>
                        </HStack>

                        <HStack gap='20px'>
                            <VStack alignItems='unset'>
                                <FormLabel>First Name</FormLabel>
                                <Input id={'new_first_name'}/>
                            </VStack>

                            <VStack alignItems='unset'>
                                <FormLabel>Last Name</FormLabel>
                                <Input id={'new_last_name'}/>
                            </VStack>
                        </HStack>

                        <VStack alignItems='unset'>
                            <FormLabel>Password</FormLabel>
                            <Input id={'new_password'} type='password'/>
                        </VStack>
                    </VStack>
                </ModalBody>

                <ModalFooter>
                    <Button colorScheme='blue' onClick={createUser}> Create User </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    </>;
}