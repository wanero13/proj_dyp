import React, {Component} from 'react';
import {StyleSheet, Text, View, TouchableOpacity, TextInput} from 'react-native';
import {Actions} from 'react-native-router-flux'
import ValidationComponent from 'react-native-form-validator';

export default class Login extends ValidationComponent {
    constructor(props) {
        super(props);

        this.state = {
            login: '',
            password: '',
            logged: null
        }
    };

    onLoginChange = (value) => {
        this.setState({login: value});
    };

    onPasswordChange = (value) => {
        this.setState({password: value});
    };

    onSubmitLogin = async (event) => {
        event.preventDefault();
        fetch('http://localhost:5000/api/login', {
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            credentials: "include",
            body: JSON.stringify({
                loginl: this.state.login,
                passwordl: this.state.password
            })
        }).then((response) => {
            if (!response.ok) {
                console.log(response.status);
                throw new Error(response.statusText);
            } else return response;
        }).then((responseObject) => {
            this.setState({logged: true});
            console.log(responseObject);
            console.log('inside');

            Actions.authUser();
        }).catch((error) => {
            console.log('error: ' + error);
            this.setState({logged: false});
        })
    };

    _onSubmit() {
        // Call ValidationComponent validate method
        this.validate({
            login: {minlength:4, maxlength:24, required: true, hasSpecialCharacter: false},
            password: {required: true, minlength: 8, maxlength: 16, hasNumber: true, hasSpecialCharacter: true, hasUpperCase: true},
        });
    }

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.logoText}>Login page</Text>
                <TextInput style={styles.inputBox} value={this.state.login}
                           onChangeText={this.onLoginChange} placeholder="login" placeholderTextColor='#fff5e1'/>
                <TextInput style={styles.inputBox} value={this.state.password}
                           onChangeText={this.onPasswordChange} placeholder="password" placeholderTextColor='#fff5e1'
                           secureTextEntry={true}/>
                <TouchableOpacity style={styles.button} onPress={this.onSubmitLogin.bind(this)}>
                    <Text style={styles.buttonText}>Login</Text>
                </TouchableOpacity>
                <View style={styles.signupTextCon}>
                    <TouchableOpacity onPress={Actions.signup}>
                        <Text style={styles.signupText}>Don't have an account yet? Sign up!</Text>
                    </TouchableOpacity>
                </View>
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
