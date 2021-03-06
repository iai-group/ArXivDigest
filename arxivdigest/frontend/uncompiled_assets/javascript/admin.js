$(document).ready(function () {
    $("ul.nav a[href ='#systems']").bind("show.bs.tab", function () {
        $.getJSON("/admin/systems/get", {},
            function (data) {
                if (data.success === true) {
                    generateSystemTableHtml(data.systems)
                }
            });
    });

    $("ul.nav a[href ='#admins']").bind("show.bs.tab", function () {
        $.getJSON("/admin/admins/get", {},
            function (data) {
                if (data.success === true) {
                    generateAdminsTableHtml(data.admins)
                }
            });
    });

    $(".systemList tbody").on("click", ".toggleSystem", function () {
        var box = $(this);
        box.active = !box.prop("checked");
        if (!box.active) {
            var conf = confirm("Activate system: " + box.data("value") + "?");
            if (!conf) {
                box.prop("checked", false);
                return
            }
        }
        $.ajax({
            url: "/admin/systems/toggleActive/" + box.data("value") + "/" + !box.active,
            type: 'PUT',
            success: function (data) {
                if (data.result === "Success") {
                    box.active = !box.active
                }
                if (data.err === "Email error") {
                    alert("Failed to send email.")
                }
            }
        }).always(function (d) {
            box.prop("checked", box.active);
            box.prop("title", box.prop("checked") ? "Deactivate this system." : "Activate this system.");
        });

    });

    $("ul.nav a[href ='#general']").bind("show.bs.tab", function () {
        $.getJSON("/admin/general", {},
            function (data) {
                var ctx;
                if (data.success === true) {
                    plotcontainer = $("#userPlotContainer");
                    $("#userPlot").remove();
                    plotcontainer.append("<canvas id='userPlot'></canvas>");
                    ctx = $("#userPlot")[0].getContext('2d');
                    myChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: data.users.dates,
                            datasets: [{
                                label: 'User registration over time',
                                data: data.users.users,
                               backgroundColor: 'rgba(100, 159, 64, 0.3)'
                            }]
                        },
                    });
                    plotcontainer = $("#articlePlotContainer");
                    $("#articlePlot").remove();
                    plotcontainer.append("<canvas id='articlePlot'></canvas>");
                    ctx = $("#articlePlot")[0].getContext('2d');
                    myChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: data.articles.dates,
                            datasets: [{
                                label: 'Articles scraped over time',
                                data: data.articles.articles,
                                backgroundColor: 'rgba(100, 159, 64, 0.3)'
                            }]
                        },
                    });
                    $("#statistics").html("Total users: <strong>" + data.users.total + "\n</strong> Total articles:<strong>" + data.articles.total + "</strong>")
                }
            });
    });

    $("ul.nav a[href ='#evaluation']").bind("show.bs.tab", function () {
        let evaluation_area = $("#evaluation");
        evaluation_area.empty();
        let system_list = create_system_list(evaluation_area, "/admin/systems/get", create_system_stats_plots, true);
        evaluation_area.append(system_list);
    });

    $("ul.nav a[href ='#feedback']").bind("show.bs.tab", function () {
        let evaluation_area = $("#feedback");
        evaluation_area.empty();
        let system_list = create_system_list(evaluation_area, "/admin/systems/get", create_system_feedback_plots, false, true);
        evaluation_area.append(system_list);
    });

    $(".nav-tabs a").click(function () {
        $(this).tab("show");
    });

    if (location.hash) { //switches tabs based on the anchor part (#) of url
        $("ul.nav a[href='" + location.hash + "']").tab("show");
    } else {
        const tabs = $(".nav-tabs li:first-child a");
        if (tabs) {
            tabs.tab("show");
        }
    }
})
;

function generateSystemTableHtml(systems) {
    let html = "<tr>";
    for (const system of systems) {
        html += "<td>" + system.system_id + "</td>";
        html += "<td>" + system.system_name + "</td>";
        html += "<td>" + system.firstname + " " + system.lastname + "</td>";
        html += "<td>" + system.organization + "</td>";
        html += "<td>" + system.email + "</td>";
        html += "<td>" + system.api_key + "</td>";
        html += "<td><input class='toggleSystem' type='checkbox' data-value=" + system.system_id
        if (system.active) {
            html += " checked"
        }
        html += system.active ? " title='Deactivate this system.'" : " title='Activate this system.'"
        html += "></td></tr>";
    }
    $(".systemList tbody").html(html)
}

function generateAdminsTableHtml(admins) {
    let html = "<tr>";
    for (const admin of admins) {
        html += "<td>" + admin.user_id + "</td>";
        html += "<td>" + admin.email + "</td>";
        html += "<td>" + admin.firstname + " " + admin.lastname + "</td>";
        html += "></td></tr>";
    }
    $("#admins tbody").html(html)
}
