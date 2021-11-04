var rows = 0;
var columns = 0;

if (document.getElementById("id_numbers") != null) {
    document.getElementById("id_numbers").value = '';
    document.getElementById("id_rows").value = '';
    document.getElementById("id_cols").value = '';

} else {
    document.getElementById("id_numbers1").value = '';
    document.getElementById("id_rows1").value = '';
    document.getElementById("id_cols1").value = '';
    document.getElementById("id_numbers2").value = '';
    document.getElementById("id_rows2").value = '';
    document.getElementById("id_cols2").value = '';

}

document.querySelectorAll(".get-calculate").forEach((i) => {
    i.addEventListener("click", () => {
        var vals1 = getMatrixCalculate(1);
        var valString1 = vals1.toString();
        document.getElementById("id_operator").value = i.value;
        document.getElementById("id_numbers1").value = valString1;
        document.getElementById("id_rows1").value = document.getElementById("val_m1").value;
        document.getElementById("id_cols1").value = document.getElementById("val_n1").value;
        var vals2 = getMatrixCalculate(2);
        var valString2 = vals2.toString();
        document.getElementById("id_numbers2").value = valString2;
        document.getElementById("id_rows2").value = document.getElementById("val_m2").value;
        document.getElementById("id_cols2").value = document.getElementById("val_n2").value;
        console.log(vals1);
        console.log(vals2);
    })
})

$("#set").click(function () {
    var rows = document.getElementById("val_m").value;
    var columns = document.getElementById("val_n").value;
    var form = document.getElementById("matrix_input");

    while (form.firstChild) {
        form.removeChild(form.firstChild);
    }


    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < columns; j++) {
            var input = $('<input>')
                .attr({
                    class: 'matrix_cell',
                });
            form.appendChild(input[0]);
        }
        var br = $('<br>')[0];
        form.appendChild(br);
    }

});

$("#set1").click(function () {
    let rows = document.getElementById("val_m1").value;
    let columns = document.getElementById("val_n1").value;
    let form = document.getElementById("matrix_input1");

    while (form.firstChild) {
        form.removeChild(form.firstChild);
    }


    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < columns; j++) {
            let input = $('<input>')
                .attr({
                    class: 'matrix_cell1',
                });
            form.appendChild(input[0]);
        }
        let br = $('<br>')[0];
        form.appendChild(br);
    }

});

$("#set2").click(function () {
    let rows = document.getElementById("val_m2").value;
    let columns = document.getElementById("val_n2").value;
    let form = document.getElementById("matrix_input2");

    while (form.firstChild) {
        form.removeChild(form.firstChild);
    }


    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < columns; j++) {
            let input = $('<input>')
                .attr({
                    class: 'matrix_cell2',
                });
            form.appendChild(input[0]);
        }
        let br = $('<br>')[0];
        form.appendChild(br);
    }

});

function getMatrix() {
    var matrix_row = [];

    var ind = 0;

    $("#matrix_input").contents().each(function (i, e) {
        if (this.nodeName == "INPUT") {
            if (!matrix_row[ind]) {
                matrix_row.push([]);
            }
            matrix_row[ind].push(eval(($(this).val())));
        } else {
            ind++;
        }
    });

    return matrix_row;
}

function getMatrixCalculate(i) {
    var matrix_row = [];

    var ind = 0;

    $("#matrix_input" + i).contents().each(function (i, e) {
        if (this.nodeName == "INPUT") {
            if (!matrix_row[ind]) {
                matrix_row.push([]);
            }
            matrix_row[ind].push(eval(($(this).val())));
        } else {
            ind++;
        }
    });

    return matrix_row;
}

