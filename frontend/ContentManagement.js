var elements = new Array();

function addElement(element){
    elements.push(element);
    return elements.length - 1;
}

function addGroup(){
    elements.push(new Array());
    return elements.length - 1;
}

function addToGroup(group, element){
    elements[group].push(element);
    return elements[group].length -1;
}

function empty(){
    for(var i = elements.length-1; i>=0; i--){
        if( Object.prototype.toString.call( elements[i] ) === '[object Array]' ) {
            for(var x=elements[i].length-1; x>=0; x--)
                elements[i][x].destroy();
            elements.splice(i, 1);
        }else{
            elements[i].destroy();
        }
    }
}

function deleteGroup(index){
    for(var i = elements[index].length-1; i>=0; i--){
        elements[index][i].destroy();
    }
    elements.splice(index, 1);
}
