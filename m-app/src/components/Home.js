import React, { Component } from 'react';
import {View, TouchableOpacity, Text, Button, StyleSheet, TextInput} from 'react-native';
import { Actions } from 'react-native-router-flux'


export default class Home extends Component {
    constructor(props) {
        super(props);
    }

    onSubmitLogout = (event) => {
        event.preventDefault();
        fetch("http://localhost:5000/api/logout", {
            method: 'post',
            credentials: "include"
        }).then((response) => {
            if (!response.ok) {
                throw new Error(response.statusText);
            } else return response;
        }).then((responseObject) => {
            console.log("Logged out user: " + responseObject.username)
            Actions.newUser();
        }).catch((error) => {
            console.log('error: ' + error);
        })
    }

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.text}>Welcome!</Text>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>PDF Files</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Bibliography</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={this.onSubmitLogout.bind(this)}>
                    <Text style={styles.buttonText}>Logout</Text>
                </TouchableOpacity>
            </View>
        )
    }
}
const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        backgroundColor: '#fefefe',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        fontSize: 30,
        color: '#000000',
        marginVertical: 50
    },
    button: {
        width: 260,
        backgroundColor: '#1520a6',
        borderRadius: 26,
        paddingVertical: 16,
        marginVertical:10,
    },
    buttonText: {
        fontWeight: '500',
        color: '#fff5e1',
        fontSize: 20,
        textAlign: 'center',
    }
});
