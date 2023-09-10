import {
    Box,
    BoxProps,
    Input,
    FormLabel,
    HStack,
    VStack,
    Button,
    Center,
    Flex,
    Text,
    Spacer,
    useToast
} from "@chakra-ui/react"  
import { useEffect, useState } from "react";

import { AlertPopupButton } from "../AlertPopupButton";

import { User } from "../../models/User";
import { UserService } from "../../services/UserService";
import { AuthService } from "../../services/AuthService";

export const ProfileSettingsCard = (props: BoxProps) => {
    const [user, setUser] = useState<User | null>(null);
    const toast = useToast();

    useEffect(() => {
        AuthService.getLoggedInUser().then(loggedInUser => {
            if ((loggedInUser != null) && (loggedInUser.first_name != null)) {
                setUser(loggedInUser);

                var i = document.getElementById('profile-first_name') as any;
                i.value = loggedInUser.first_name;
                
                i = document.getElementById('profile-last_name') as any;
                i.value = loggedInUser.last_name;
            }
        });
    }, []);

    const updateUser = (e: any) => {
        e.preventDefault();
        
        const new_user: User = {
            username: user?.username as string,
            first_name: (document.getElementById('profile-first_name') as any).value,
            last_name: (document.getElementById('profile-last_name') as any).value,
            role: user?.role,
        }

        UserService.updateUser(user?.username as string, new_user).then(v => {
            if (v == true) {
                toast({
                    title: 'Profile Updated Successfully',
                    description: 'Your profile information has been updated successfully.',
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
            } else {
                toast({
                    title: 'Issue Encountered',
                    description: 'Could not update profile. Please check the logs for more information.',
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                });
            }
        });
    };

    const changePassword = (e: any) => {
        e.preventDefault();
        
        const password: string = (document.getElementById('profile-password') as any).value
        UserService.changePassword(user?.username as string, password).then(v => {
            if (v == true) {
                toast({
                    title: "Your Password Updated Successfully",
                    description: "Your password has been updated successfully.",
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
            } else {
                toast({
                    title: 'Issue Encountered',
                    description: "Could not update your password. Please check the logs for more information.",
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                });
            }
        });
    };

    return <Box borderWidth='1px' borderRadius='lg' padding='10px' width='fit-content'>
        <VStack gap='15px' alignItems='center'>
            <Flex flexDirection='row' width='full'>
                <Text>
                    {user?.username}    
                </Text>
            </Flex>

            <HStack gap='20px'>
                <VStack alignItems='unset'>
                    <FormLabel>First Name</FormLabel>
                    <Input id='profile-first_name'/>
                </VStack>

                <VStack alignItems='unset'>
                    <FormLabel>Last Name</FormLabel>
                    <Input id='profile-last_name'/>
                </VStack>
            </HStack>
        
            <Button colorScheme='blue' size='md' maxWidth='500px' width='full' marginBottom='25px' onClick={updateUser}> Update User </Button>

            <VStack alignItems='unset' width='full'>
                <FormLabel>Password</FormLabel>
                <Input placeholder='New Password' id='profile-password' type='password'/>
                
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