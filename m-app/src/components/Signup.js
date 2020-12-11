import React, {Component} from 'react';
import {StyleSheet, Text, View, TouchableOpacity, TextInput} from 'react-native';
import {Actions} from 'react-native-router-flux'
import ValidationComponent from 'react-native-form-validator';

export default class Signup extends ValidationComponent {
    constructor(props) {
        super(props);

        this.state = {
            login: '',
            password: '',
            email: '',
            confirm_password: '',
            errors: [],
            added: null
        }
    }

    onLoginChange = (value) => {
        this.setState({login: value});
    };
    onPasswordChange = (value) => {
        this.setState({password: value});
    };
    onConfirmChange = (value) => {
        this.setState({confirm_password: value});
    };
    onEmailChange = (value) => {
        this.setState({email: value})
    };

    onSubmitRegister = async (event) => {
        event.preventDefault();

        fetch('http://localhost:5000/api/register', {
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            credentials: "include",
            body: JSON.stringify({
                login: this.state.login,
                password: this.state.password,
                confirm_password: this.state.confirm_password,
                email: this.state.email
            })
        }).then((response) => {
            if (!response.ok) {
                throw new Error(response.statusText);
            } else return response;
        }).then((responseObject) => {
            this.setState({added: true});
            console.log(responseObject);
            console.log(typeof (responseObject.username));
            Actions.login();
        }).catch((error) => {
            console.log('error: ' + error);
            this.setState({added: false});
        });
        this.setState({errors: []})

    };

    _onSubmit() {
        // Call ValidationComponent validate method
        this.validate({
            login: {minlength:3, maxlength:7, required: true, hasSpecialCharacter: false},
            password: {required: true, minlength: 8, maxlength: 16, equalPassword(password, confirm) {
                    return false;
                }, hasNumber: true, hasSpecialCharacter: true, hasUpperCase: true},
            confirm: {required: true, minlength: 8, maxlength: 16, hasNumber: true, hasSpecialCharacter: true, hasUpperCase: true},
            email: {email: true},
        });
    }

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.logoText}>Registration page</Text>
                <TextInput style={styles.inputBox} value={this.state.login}
                           onChangeText={this.onLoginChange} placeholder="login" placeholderTextColor='#fff5e1'/>
                <TextInput style={styles.inputBox} value={this.state.password}
                           onChangeText={this.onPasswordChange} placeholder="password" placeholderTextColor='#fff5e1' secureTextEntry={true}/>
                <TextInput style={styles.inputBox} value={this.state.confirm}
                           onChangeText={this.onConfirmChange} placeholder="confirm" placeholderTextColor='#fff5e1' secureTextEntry={true}/>
                <TextInput style={styles.inputBox} value={this.state.email}
                           onChangeText={this.onEmailChange} placeholder="email" placeholderTextColor='#fff5e1'/>
                <TouchableOpacity style={styles.button} onPress={this.onSubmitRegister.bind(this)}>
                    <Text style={styles.buttonText}>Create account</Text>
                </TouchableOpacity>
                <View style={styles.textCon}>
                    <TouchableOpacity onPress={Actions.pop}>
                        <Text style={styles.footerText}>Already have an account? Sign in!</Text>
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
        marginVertical: 60,
        fontSize: 30,
        color: '#000000',
    },
    textCon: {
        flexGrow: 1,
        alignItems: 'center',
        justifyContent: 'flex-end',
        marginVertical: 40,
    },
    footerText: {
        color: '#102030',
        fontSize: 16,
    },
    inputBox: {
        width: 320,
        backgroundColor: '#102030',
        fontSize: 16,
        borderRadius: 20,
        paddingHorizontal: 10,
        marginVertical: 8,
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
