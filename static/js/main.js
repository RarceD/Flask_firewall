//I create the global store json data example:
var data = {
  client: "xxxxxxxxxxxxxxxxxxxxxxx",
  uuid: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  prog: "A",
  action: 0,
};
//The struct to hold the diferent json options
var json_options = {
  MANPROG: 0,
  MANVALVE: 1,
  GENERAL: 2,
  STOP: 3,
  PROGRAM: 4,
  AA: 5,
};
// When the dom update I generate the first data
window.onload = function () {
  document.getElementById("json_example").textContent = JSON.stringify(
    data,
    undefined,
    2
  );
  console.log("__init__");
};


function change_request(item) {
  data = {};
  switch (item) {
    case json_options.MANPROG:
      data = {
        client: "xxxxxxxxxxxxxxxxxxxxxxx",
        uuid: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        prog: "A",
        action: 0,
      };
      break;
    case json_options.MANVALVE:
      data = {
        client: "xxxxxxxxxxxxxxxxxxxxxxx",
        uuid: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        valves: [
          {
            v: 1,
            action: 1,
            time: "11:59",
          },
          {
            v: 2,
            action: 1,
            time: "01:01",
          },
        ],
      };
      break;
    case json_options.GENERAL:
      data = {
        client: "xxxxxxxxxxxxxxxxxxxxxxx",
        uuid: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        pause: 1,
        pump_delay: -20,
        valve_delay: 10,
        fertirrigations: "01010101000200020003000300040004",
        fertirrigation_number: 4,
        date: "31/07/2020 15:29",
        pump_ids: "0004040404040504",
        master_pump_associations: "00000000000000000000000000000000",
      };
      break;
    case json_options.STOP:
      data = {
        client: "xxxxxxxxxxxxxxxxxxxxxxx",
        uuid: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        stop: 1,
      };
      break;
    case json_options.PROGRAM:
      data = {
        client: "xxxxxxxxxxxxxxxxxxxxxxx",
        uuid: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        prog: "C",
        starts: ["12:32", "13:45", "05:23", "03:53", "09:45", "04:23"],
        water: 50,
        interval: 1,
        interval_init: 5,
        week_day: [1, 2, 3, 5, 7],
        valves: [
          {
            v: 1,
            time: "01:45",
          },
          {
            v: 2,
            time: "01:45",
          },
          {
            v: 3,
            time: "01:45",
          },
          {
            v: 4,
            time: "01:45",
          },
        ],
        from: "20/03",
        to: "30/09",
      };
      break;
    default:
      data = {
        not: "not",
        not: "not",
      };
      break;
  }
  document.getElementById("json_example").textContent = JSON.stringify(
    data,
    undefined,
    2
  );
}
