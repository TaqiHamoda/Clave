import {
  Flex,
  Text,
  VStack,
  SimpleGrid,
  Spacer
} from "@chakra-ui/react";

import { useState, useEffect } from "react";

import { AlertPopupButton } from "../components/AlertPopupButton";
import { ProfileSettingsCard } from "../components/settings/ProfileSettings";
import { AccountSettings } from "../components/settings/AccountsSettings";
import { InterfaceSettings } from "../components/settings/InterfaceSettings";
import { ServerResources } from "../components/settings/ServerResources";

import { Page } from "../components/Page";

import { User, UserRole } from "../models/User";
import { AuthService } from "../services/AuthService";


interface SettingsObject{
  name: string,
  component: React.ReactElement
}

export const SettingsPage = () => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    AuthService.getLoggedInUser().then(u => setUser(u));
  }, []);

  const userSettingsObjects: SettingsObject[] = [
    {
      name: "Server Resources",
      component: <ServerResources />
    }
  ];

  const adminSettingsObjects: SettingsObject[] = [
    {
      name: "Users",
      component: <AccountSettings />
    },
    {
      name: "Interfaces",
      component: <InterfaceSettings />
    }
  ];

  var settingsObjects: SettingsObject[] = userSettingsObjects;

  if( user?.role == UserRole.admin){
    settingsObjects = adminSettingsObjects.concat(settingsObjects);
  } else {
    settingsObjects = [{
      name: "Profile",
      component: <ProfileSettingsCard />
    }].concat(settingsObjects);
  }

  const logout = (e: any) => {
    e.preventDefault();

    AuthService.logout().then(result => {
        if (result) {
            window.location.reload();
        }
    });
  }
  
  return <Page>
    <Flex>
      <Spacer/>

      <AlertPopupButton
          text='Logout'
          header='Logout'
          body="Are you sure you want to logout?"
          aria-label='Logout'
          title='Logout'
          colorScheme='red'
          variant='outline'
          maxWidth='200px'
          width='full'
          size='md'
          margin='10px'
          onClick={logout}>
              Logout
      </AlertPopupButton>
    </Flex>

    <SimpleGrid columns={[1]} spacing='30px' padding='20px'>
      {
        settingsObjects.map(o => <VStack alignItems='unset'>
          <Flex width='full'>
            <Text fontFamily='monospace' fontSize='xl' fontWeight='medium'>
              {o.name}
            </Text>  
          </Flex>

          {o.component}          
        </VStack>)
      }
    </SimpleGrid>
  </Page>
}
