import React, {Component} from 'react';
import {View, TouchableOpacity, Text, Button, StyleSheet, TextInput, FlatList} from 'react-native';
import {Actions} from 'react-native-router-flux';


export default class Note extends Component {
    constructor(props) {
        super(props);
        this.state = {
            note_id: props.note_id,
            note: []
        };
    }

    componentDidMount = async () => {
        await this.loadNote();
    };

    loadNote = async () => {
        let note_id=this.state.note_id
        try {
            const response = await fetch(`http://localhost:5000/api/note/${note_id}`, {
                method: 'GET',
                credentials: "include",
            });
            var data = await response.json();
            this.setState({note: data})
            console.log(this.state.note)
        } catch (error) {
            console.log(error);
        }
    };

    render() {
        let noteElement = <Text>Can't find this note.</Text>;
        if (this.state.note.length > 0) {
            let note = this.state.note
            noteElement = <View style={styles.container}>
                <Text style={styles.buttonText}>
                    Author: {note[1]}
                </Text>
                <Text style={styles.buttonText}>
                    Title: {note[3]}
                </Text>
                <Text style={styles.buttonText}>
                    Content: {note[4]}
                </Text>
                    </View>}
        return (
            <View style={styles.container}>
                {noteElement}
            </View>
        )
    }
}
const styles = StyleSheet.create({
    logoText: {
        marginVertical: 100,
        fontSize: 30,
        color: '#000000',
    },
    container: {
        flex: 1,
        backgroundColor: '#fefefe',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        flexGrow: 1,
        fontSize: 20,
        color: '#000000'
    },
    button: {
        width: 300,
        backgroundColor: '#1520a6',
        borderRadius: 26,
        paddingVertical: 16,
        marginVertical: 10,
        color: '#ffffff'
    },
    buttonText: {
        fontWeight: '500',
        color: '#000000',
        fontSize: 20,
        textAlign: 'center',
    },
    addButton: {
        width: 160,
        backgroundColor: '#000000',
        borderRadius: 20,
        paddingVertical: 10,
        marginVertical: 10,
        color: '#ffffff',
        textAlign: 'center'
    },
    addText: {
        color: '#ffffff',
        fontSize: 20,
        textAlign: 'center',
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
});
