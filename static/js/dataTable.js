$(document).ready(function() {
    // Handle table selection
    $('#table-select').change(function() {
        var tableName = $(this).val();
        if (tableName) {
            $.ajax({
                url: '/fetch_table',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ table_name: tableName }),
                success: function(data) {
                    updateResults(data);
                },
                error: function() {
                    alert('Error fetching data.');
                }
            });
        }
    });

    // Handle query execution
    $('#execute-button').click(function() {
        var sqlQuery = $('#sql_query').val();
        $.ajax({
            url: '/execute_query',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: sqlQuery }),
            success: function(data) {
                updateResults(data);
            },
            error: function() {
                alert('Error executing query.');
            }
        });
    });

    // Handle button execution
    $('#query1-button').click(function() {
        $.ajax({
            type: 'POST',
            url: '/query1',
            success: function(data) {
                updateResults(data);
                $('#sql_query').val(data.output_query);
            },
            error: function(error) {
                console.log("Error:", error);
            }
        });
    });

    $('#query2-button').click(function() {
        $.ajax({
            type: 'POST',
            url: '/query2',
            success: function(data) {
                updateResults(data);
                $('#sql_query').val(data.output_query);
            },
            error: function(error) {
                console.log("Error:", error);
            }
        });
    });

    $('#query3-button').click(function() {
        $.ajax({
            type: 'POST',
            url: '/query3',
            success: function(data) {
                updateResults(data);
                $('#sql_query').val(data.output_query);
            },
            error: function(error) {
                console.log("Error:", error);
            }
        });
    });

    $('#query4-button').click(function() {
        $.ajax({
            type: 'POST',
            url: '/query4',
            success: function(data) {
                updateResults(data);
                $('#sql_query').val(data.output_query);
            },
            error: function(error) {
                console.log("Error:", error);
            }
        });
    });
    
    // Function to update results table
    function updateResults(data) {
        if (data.error) {
            alert(data.error);
            return;
        }
        $('#results-header').empty();
        $('#results-body').empty();

        // Add headers
        data.columns.forEach(function(column) {
             $('#results-header').append('<th>' + column + '</th>');
        });

        // Add rows
        data.results.forEach(function(row) {
            var tr = $('<tr></tr>');
            row.forEach(function(cell) {
                tr.append('<td>' + cell + '</td>');
            });
            $('#results-body').append(tr);
        });
    }
});


## Test Only
$(document).ready(function() {
    $('.load-content-btn').on('click', function(event) {
        event.preventDefault();
        var url = $(this).data('url');
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                console.log(data);
                $('#content-div').html(data);
                const items = $('#content-div').find('.item');

                items.each(function(index, item) {
                    const $item = $(item).addClass('fade-in');
                    $('#content-div').append($item);
                })

                // Fade in items as they scroll into view
                fadeInOnScroll();
            },
            error: function(error) {
                console.log("Error:", error);
            }
        });
    });
});

            <div class="navbar__card">
                <nav>
                    <a class="load-content-btn" data-url="/about">About Me</a>
                    <a class="load-content-btn" data-url="/project">Projects</a>
                    <a class="load-content-btn" data-url="/certificate">Certificates</a>
                    <a class="load-content-btn" data-url="/load-content">Hobbies</a>
                    <a class="load-content-btn" data-url="/load-content">blog</a>
                    <a class="load-content-btn" data-url="/load-content">Hire Me!</a>
                    <div class="animation start-home"></div>
                </nav>
            </div>
            <div class="main__card" id="content-div">
            </div>
