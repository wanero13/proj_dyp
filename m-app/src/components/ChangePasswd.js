import React, {Component} from 'react';
import {StyleSheet, Text, View, TouchableOpacity, TextInput} from 'react-native';
import {Actions} from 'react-native-router-flux'
import ValidationComponent from 'react-native-form-validator';
import AsyncStorage from "@react-native-community/async-storage";

export default class ChangePasswd extends ValidationComponent {
    constructor(props) {
        super(props);

        this.state = {
            login: '',
            password: '',
            new_password: '',
            confirm_password: '',
        }
    };

    onLoginChange = (value) => {
        this.setState({login: value});
    };

    onCurrPasswordChange = (value) => {
        this.setState({password: value});
    };

    onNewPasswordChange = (value) => {
        this.setState({new_password: value});
    };

    onConfPasswordChange = (value) => {
        this.setState({confirm_password: value});
    };


    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.logoText}>Change your password</Text>
                <TextInput style={styles.inputBox} value={this.state.password}
                           onChangeText={this.onCurrPasswordChange} placeholder="current password" placeholderTextColor='#fff5e1'
                           secureTextEntry={true}/>
                <TextInput style={styles.inputBox} value={this.state.new_password}
                           onChangeText={this.onNewPasswordChange} placeholder="new password" placeholderTextColor='#fff5e1'
                           secureTextEntry={true}/>
                <TextInput style={styles.inputBox} value={this.state.confirm_password}
                           onChangeText={this.onConfPasswordChange} placeholder="confirm new password" placeholderTextColor='#fff5e1'
                           secureTextEntry={true}/>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Change Password</Text>
                </TouchableOpacity>
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
    }
});
