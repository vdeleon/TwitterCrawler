// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item{
    id: root
    width: parent.width
    height: 30
    signal selectedValueChanged(int value);
    RadioGroup{
        id: radioGroup
        onSelectedValueChanged: {
            root.selectedValueChanged(selectedValue);
        }
    }
    Row{
        id: searchOptions
        anchors.fill: parent
        RadioButton{
            width: root.width/2
            text: "Mappa"
            group: radioGroup
            value: 1
        }
        RadioButton{
            width: root.width/2
            text: "Contenuto"
            group: radioGroup
            value: 2
        }
    }
}
