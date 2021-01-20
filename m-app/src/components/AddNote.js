import React, {Component} from 'react';
import {StyleSheet, Text, View, TouchableOpacity, TextInput, CheckBox} from 'react-native';
import {Actions} from 'react-native-router-flux'
import ValidationComponent from 'react-native-form-validator';
import AsyncStorage from "@react-native-community/async-storage";
import FlashMessage from "react-native-flash-message";
import { showMessage, hideMessage } from "react-native-flash-message";


export default class AddNote extends ValidationComponent {
    constructor(props) {
        super(props);

        this.state = {
            title: '',
            content: '',
            isPrivate: false
        }
    };

    onTitleChange = (value) => {
        this.setState({title: value});
    };

    onContentChange = (value) => {
        this.setState({content: value});
    };

    onIsPrivateChange = (value) => {
        this.setState({isPrivate: value});
    };

    _onSubmitNote() {
        this.validate({
            title: {minlength:3, maxlength:30, required: true, hasSpecialCharacter: false},
            content: {minlength:3, maxlength:300, required: true, hasSpecialCharacter: false},
        });
    }


    onSubmitNote = async (event) => {
        event.preventDefault();
        this._onSubmitNote()
        if (!this.isFormValid()){
            return
        }
        let cookie = await AsyncStorage.getItem('cookie');
        fetch('https://localhost:5000/api/addnote', {
            method: 'post',
            headers: {'Content-Type': 'application/json', 'Cookie': cookie},
            credentials: "include",
            body: JSON.stringify({
                title: this.state.title,
                content: this.state.content,
                isPrivate: this.state.isPrivate
            })
        }).then((response) => {
            if (!response.ok) {
                console.log(response.status);
                throw new Error(response.statusText);
            } else return response;
        }).then((responseObject) => {
            if (responseObject.status === 422) {
                console.log(responseObject.body)
            } else if (responseObject.status === 400) {
                showMessage({
                    message: "Operation Failed",
                    type: "danger",
                    autoHide: true,
                    duration: 1000
                });
            } else if (responseObject.status===401) {
                Actions.newUser()
            } else {
                showMessage({
                    message: "Note added successfully!",
                    type: "success",
                    autoHide: true,
                    duration: 1000
                });
            }
        }).catch((error) => {
            console.log('error: ' + error);
            this.setState({logged: false});
        })
    };

    _onSubmit() {
        // Call ValidationComponent validate method
        this.validate({
            login: {minlength: 4, maxlength: 24, required: true, hasSpecialCharacter: false},
            password: {
                required: true,
                minlength: 8,
                maxlength: 16,
                hasNumber: true,
                hasSpecialCharacter: true,
                hasUpperCase: true
            },
        });
    }

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.logoText}>Add your note</Text>
                <TextInput style={styles.inputBox} value={this.state.title}
                           onChangeText={this.onTitleChange} placeholder="title" placeholderTextColor='#fff5e1'/>
                <TextInput style={styles.textInput} value={this.state.text}
                           onChangeText={this.onContentChange} placeholder="content" placeholderTextColor='#fff5e1'
                           multiline={true} numberOfLines={4}/>
                <CheckBox style={styles.checkbox} value={this.state.isPrivate} onValueChange={this.onIsPrivateChange}>
                </CheckBox>
                <Text style={styles.label}>Is note private?</Text>
                <TouchableOpacity style={styles.button} onPress={this.onSubmitNote.bind(this)}>
                    <Text style={styles.buttonText}>Submit Note</Text>
                </TouchableOpacity>
                <FlashMessage position="center" />
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    logoText: {
        marginVertical: 100,
        fontSize: 30,
        color: '#000000',
    },
    signupTextCon: {
        flexGrow: 1,
        alignItems: 'center',
        justifyContent: 'flex-end',
        marginVertical: 40,
    },
    signupText: {
        color: '#102030',
        fontSize: 16,
    },
    inputBox: {
        width: 320,
        backgroundColor: '#102030',
        fontSize: 16,
        borderRadius: 20,
        paddingHorizontal: 10,
        marginVertical: 12,
        height: 50,
        color: '#ffffff'
    },
    textInput: {
        width: 320,
        backgroundColor: '#102030',
        fontSize: 16,
        borderRadius: 20,
        paddingHorizontal: 10,
        marginVertical: 12,
        textAlignVertical: 'top',
        maxHeight: 300,
        color: '#ffffff'
    },
    button: {
        width: 320,
        backgroundColor: '#1520a6',
        borderRadius: 20,
        paddingVertical: 12,
        marginVertical: 8,
    },
    buttonText: {
        fontWeight: '500',
        color: '#fff5e1',
        fontSize: 20,
        textAlign: 'center',
    },
    checkbox: {
        alignSelf: "center",
    },
    label: {
        margin: 8,
    },
});
