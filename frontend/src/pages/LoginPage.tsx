import { useState, useEffect } from "react"
import { useNavigate, useLocation } from "react-router"
import { useAuth } from "../components/Authentication"
import {
  Box,
  VStack,
  Button,
  FormControl,
  FormLabel,
  Input,
  Image,
  Flex,
} from "@chakra-ui/react"

import Logo from "../static/Open-CR-Logo.svg"
import { ColorModeSwitcher } from "../components/ColorModeSwitcher"

import { User } from "../models/User"
import { ENV } from "../services/Environment"

export const LoginPage = () => {

  const [submitting, setSubmitting] = useState<boolean>(false);

  const auth = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const onSubmit = async (e: any) => {
    e.preventDefault();
    setSubmitting(true);

    const user: User = {
      username: e.target.username.value,
      password: e.target.password.value
    }

    try {
      auth.signin(user, result => {
        setSubmitting(false);
        console.log(auth.user);

        if (result != null) {
          navigate(ENV.HOME_PATH, { replace: true });
        } else {
          alert("Incorrect login.");
        }
      });
    } catch (e) {
      setSubmitting(false);
      console.log(e);
    }
  };

  useEffect(() => {
    auth.signedin(result => {
      if(result != null){
        let to = (location.state as any)?.from?.pathname || ENV.HOME_PATH;
        navigate(to, { replace: true });
      }
    });
  }, []);

  return (
    <Box textAlign="center">
      <VStack spacing={8}>
        <Flex width='full' direction='row-reverse' padding='10px'>
          <ColorModeSwitcher />
        </Flex>
        <Image src={Logo} h="40vmin" pointerEvents="none" />

        <form onSubmit={onSubmit}>
          <VStack spacing={5}>
            <FormControl>
              <FormLabel htmlFor='text'>Username</FormLabel>
              <Input id='username' type='text' />
            </FormControl>

            <FormControl>
              <FormLabel htmlFor='password'>Password</FormLabel>
              <Input id='password' type='password' />
            </FormControl>

            <Button marginTop={4} colorScheme='blue' isLoading={submitting} type='submit'>
              Login
            </Button>
          </VStack>
        </form>
      </VStack>
    </Box>
  )
}
