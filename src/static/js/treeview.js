export function treeview()
{
    var toggler = document.getElementsByClassName("caret");
    var all = document.getElementsByTagName("li");
    var i;

    for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function() {
        this.parentElement.querySelector(".nested").classList.toggle("active");
        this.classList.toggle("caret-down");
    });
    } 

    
}