import React, {Component} from 'react';
import {StyleSheet, Text, View, TouchableOpacity, TextInput, CheckBox} from 'react-native';
import {Actions} from 'react-native-router-flux'
import ValidationComponent from 'react-native-form-validator';
import AsyncStorage from "@react-native-community/async-storage";

export default class ChangePasswd extends ValidationComponent {
    constructor(props) {
        super(props);
    };

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.logoText}>BLANK</Text>
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
