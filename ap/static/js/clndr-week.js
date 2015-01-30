var clndr = $('#clndr').clndr({
    template: $('#clndr-template').html(),

    extras: {
        currentWeek: moment(),
    },

    daysOfTheWeek: ['LD', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'],

    doneRendering: function() {
        /* Next button handler */
        $('#clndr .clndr-next-button').on('click', function() {
            // add a week to currentWeek
            clndr.options.extras.currentWeek.add('weeks', 1);
            clndr.setMonth(clndr.options.extras.currentWeek.month());
            clndr.render();
        });

        /* Previous button handler */
        $('#clndr .clndr-previous-button').on('click', function() {
            // subtract a week to currentWeek
            clndr.options.extras.currentWeek.subtract('weeks', 1);
            clndr.setMonth(clndr.options.extras.currentWeek.month());
            clndr.render();
        });
    }
});