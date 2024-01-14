import React, { useState } from "react";
import { Upload, Form, Input, Select, message, Button } from "antd";
import { busNames, busRoutes } from "../../utils/constants";
import { FaUpload } from 'react-icons/fa';
import { v4 as uuidv4 } from 'uuid';
import axios from "axios";

type FormValues = {
    studentFirstName: string;
    studentLastName: string;
    busNumber: string;
    busStop: string;
    studentImages: string | ArrayBuffer | null; 
};

const { Dragger } = Upload;

const BusRegistration = () => {

    const [selectedBusName, setSelectedBusName] = useState(null);
    const [studentImageBase64, setStudentImageBase64] = useState<string | null>(null);
    const BACKEND_URL = "http://localhost:5000"


    const handleBusNumberChange = (value : any) => {
        setSelectedBusName(value);
        form.resetFields(['busStop']); 
    };

    const [formValues, setFormValues] = useState<FormValues>({
        studentFirstName: "",
        studentLastName: "",
        busNumber: "",
        busStop: "",
        studentImages: null,
    });

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const customValidator = (message : string) => (_: any, value: any) => {
        if (!value || value.trim() === '') {
          return Promise.reject(new Error(message));
        }
        return Promise.resolve();
    };

    const [form] = Form.useForm();

    // TODO: mayybe have an add child? nah idk... (reset the form and allow to enter another child?)

    const onFinish = (values: FormValues) => {
        console.log("Received values of form: ", values);
        // submit the form and check the values
        const busStopValue = Number(values.busStop.split(" ")[2]) - 1;

        // when sendign to db, do values.busNumber -> .split(" ")[1] to gt the number
        const submissionData = {
            id: uuidv4(),
            student_name: values.studentFirstName + " " + values.studentLastName,
            encoded_image: studentImageBase64?.split(",")[1],
            bus_number: Number(values.busNumber.split(" ")[1]),
            bus_stop: busStopValue,
            // on bus? default to false
        };

        console.log("Received values of form: ", submissionData);
    
        // filter the results if needed here with if (values.field === ....); erorrMsg return;
        // upload the data to the DB here\
        try {
            axios.post(`${BACKEND_URL}/add_row`, submissionData);
            message.success("Successfully registered new bus passenger!");
        } catch (error) {
            console.log(error);
            message.error("Failed to register new bus passenger, try again!");
        }
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const onFinishFailed = (errorInfo: any) => {
        console.log("Failed:", errorInfo);
        message.error("Failed to register new bus passenger, try again!");
    }

    const selectedBusStops = selectedBusName
    ? busRoutes.find((route) => route.name === selectedBusName)?.stops || []
    : [];

    const SUPPORTED_FILE_TYPES = ['image/png', 'image/jpg', 'image/jpeg'];

    const props = {
        onRemove: (file: any) => {
            setFormValues({
                ...formValues,
                studentImages: null,
            });
        },
        beforeUpload: (file: any) => {
            if (!SUPPORTED_FILE_TYPES.includes(file.type)) {
                message.error(`${file.type} is not a valid format`);
                return Upload.LIST_IGNORE;
            }
            const isLt2M = file.size / 1024 / 1024 < 2;
            if (!isLt2M) {
                message.error('Your image must be smaller than 2MB!');
                return Upload.LIST_IGNORE;
            }

            const reader = new FileReader();
            reader.onload = () => {
                setStudentImageBase64(reader.result as string);
            };
            reader.onerror = (error) => {
                message.error('Error reading file: ' + error);
            };
            reader.readAsDataURL(file);
            return false;

        },
    };

    return (
        <section className="bus section">
            <div className="flex flex-col items-center justify-center ">
                <h2 className="text-3xl font-bold mb-4">Bus Registration</h2>
                <h3 className="text-sm font-semibold mb-4">Register your child for the bus. more filler text here...</h3>
                <Form 
                    form={form}
                    layout="vertical"
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
                    onValuesChange={(changedValues: Partial<FormValues> ) => {                        
                        const updatedFormValues = { ...formValues, ...changedValues };
                        setFormValues(updatedFormValues);
                        console.log(updatedFormValues);
                    }}
                >
                    <Form.Item 
                        label={<p className="font-semibold">Student First Name</p>}
                        name="studentFirstName"
                        rules={[{ validator: customValidator("Please enter your child's first name!") }]}   
                    >
                        <Input className="border border-gray-400 pl-3 py-1 rounded-2xl" placeholder="John"/>
                    </Form.Item>
                 
                    <Form.Item 
                        label={<p className="font-semibold"> Student Last Name </p>}
                        name="studentLastName" 
                        rules={[{ validator: customValidator("Please enter your child's last name!") }]}   
                    >
                        <Input className="border border-gray-400 pl-3 py-1 rounded-2xl" placeholder="Smith"/>
                    </Form.Item>

                    <Form.Item label="Bus Number" 
                        name="busNumber" 
                        className="font-semibold"
                        rules={[{ validator: customValidator("Please select a bus route!") }]}   
                    >
                        <Select onChange={handleBusNumberChange} placeholder="Bus 1" className="rounded-2xl" >
                            {busNames.map((bus, index) => (
                                <Select.Option key={index} value={bus} className="rounded-2xl" >
                                    {bus}
                                </Select.Option>
                            ))}
                        </Select>
                    </Form.Item>

                    <Form.Item 
                        label="Bus Stop" 
                        name="busStop" 
                        className="font-semibold"
                        rules={[{ validator: customValidator("Please select a bus stop!") }]}   
                    >
                        <Select 
                            disabled={!selectedBusName} 
                            placeholder={selectedBusName ? "Select a stop" : "Please select a bus route first"}
                            className="rounded-2xl"
                        >
                            {selectedBusStops.map((stop, index) => (
                                <Select.Option key={index} value={stop.label} className="rounded-2xl">
                                    {stop.children}
                                </Select.Option>
                            ))}
                        </Select>
                    </Form.Item>

                    <Form.Item 
                         label="Student Image" 
                         name="studentImages" 
                         className="font-semibold"
                    >
                        <Dragger {...props} 
                            maxCount={1} 
                            className='h-42 w-42'>
                            <p className="ant-upload-drag-icon flex items-center justify-center">
                                <FaUpload className="text-4xl text-green-300"/>
                            </p>
                            <p className="ant-upload-text p-1 font-medium">Click or drag file to upload</p>
                            <p className="ant-upload-hint px-10">
                                Drag and drop your PNG or JPEG file here, or click to select it. (2 MB limit)
                            </p>
                        </Dragger>
                    </Form.Item>

                    <Form.Item>
                        <Button 
                            className="bg-green-400 text-white font-semibold rounded-md hover:bg-green-500 items-center justify-center"
                            htmlType="submit"
                        >
                            Register
                        </Button>
                    </Form.Item>
                </Form>
            </div>
        </section>
    )
}

export default BusRegistration;