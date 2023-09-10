import {
  Badge,
  SimpleGrid,
  Text,
  HStack,
  Skeleton,
  VStack,
  Input,
  InputGroup,
  InputRightElement,
  Flex,
  Spacer,
  useToast
} from "@chakra-ui/react";
import { useState, useEffect } from "react";
import { Search, CloudUploadFill } from 'react-bootstrap-icons';

import { Report } from "../models/Report";
import { ReportService } from "../services/ReportService";

import { Page } from "../components/Page";
import { ClickableCard } from "../components/ClickableCard";
import { FileUploadIconButton } from "../components/FileUploadIconButton";
import { ENV } from "../services/Environment";

export const ReportsPage = () => {
  // TODO: Add Sort (Ascending and Descending) Functionality and Filter by Module
  const [searchReports, setSearchReports] = useState<Report[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loaded, setLoaded] = useState<boolean>(false);

  const [uploading, setUploading] = useState<boolean>(false);
  const toast = useToast();

  useEffect(() => {
    ReportService.getReports().then(result => {
      if (result != null) {
        setSearchReports(result);
        setReports(result);
        setLoaded(true);
      }
    });
  }, []);

  const onSearch = (e: any) => {
    e.preventDefault();

    const keyword: string = e.target.value;
    if(keyword.length == 0){
      setSearchReports(reports);
      return;
    }

    const results: Report[] = [];
    setSearchReports([]);

    for(let report of reports){
      if(report.experiment.toLowerCase().includes(keyword.toLowerCase())){
        results.push(report);
        setSearchReports(results);
      }
    }
  };

  const onImport = (files: FileList | null | undefined) => {
    if(files == null || files.length == 0) { return; }

    setUploading(true);

    const formData = new FormData();

    Array.from(files).forEach(file => {
      formData.append(file.name, file);
    });

    console.log(formData);

    ReportService.uploadReports(formData).then(result => {
      setUploading(false);

      if(result){
        toast({
          title: 'Report Imported Successfully',
          description: 'The report has been imported successfully. The data should be found in the reports page.',
          status: 'info',
          duration: 9000,
          isClosable: true,
        });
      } else{
        toast({
          title: 'Issue Encountered',
          description: 'An error was encountered while uploading the report data. Please ensure that no duplicates with the same name exist.',
          status: 'error',
          duration: 9000,
          isClosable: true,
        });
      }
    });
  }

  return <Page>
    <Flex padding='25px'>
      <Spacer/>
      
      <InputGroup maxWidth='500px'>
        <Input placeholder='Search Reports' onChange={onSearch} />
        <InputRightElement children={<Search />} />
      </InputGroup>

      <Spacer/>

      <FileUploadIconButton
      aria-label="Import Report Data."
      title="Import Report"
      size="lg"
      fontSize="lg"
      icon={<CloudUploadFill/>}
      multiple
      accept=".zip"
      isLoading={uploading}
      onClick={onImport}/>
    </Flex>

    <Skeleton
      margin={reports.length > 0 ? undefined : '100px'}
      height={reports.length > 0 ? undefined : '150px'}
      isLoaded={loaded}>

      <SimpleGrid columns={[1, 2, 3, 4]} gap='25px' padding='25px'>
        {searchReports.map(report =>
          <ClickableCard
            borderRadius='lg'
            to={`${ENV.REPORTS_PATH}/${report.experiment}`}>
            <VStack padding='10px' alignItems='start'>
              <Text fontSize='2xl' fontFamily='monospace'>
                {report.experiment}
              </Text>
              
              <HStack >
                <Badge colorScheme={report.running ? 'orange' : 'blue'}>
                  {report.running ? 'Running Experiment' : 'Finished'}
                </Badge>
                <Badge colorScheme='gray'>
                  {`${report.datapoints} Datapoints Collected`}
                </Badge>
              </HStack>

              <HStack>
                <Badge colorScheme='purple'>
                  {report.module}
                </Badge>
                <Badge colorScheme='teal'>
                  {(new Date(report.timestamp)).toUTCString()}
                </Badge>
              </HStack>
              
            </VStack>
          </ClickableCard>
        )}
      </SimpleGrid>
    </Skeleton>
  </Page>;
}
