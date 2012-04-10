/*
Copyright (C) 2012 Riccardo Ferrazzo <f.riccardo87@gmail.com>

This file is part of TwitterCrawler.

    TwitterCrawler is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TwitterCrawler is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with TwitterCrawler.  If not, see <http://www.gnu.org/licenses/>

*/

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
