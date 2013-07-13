function select2AutocompleteManyToManyField(field, request_url) {
    var map = {};
    $("#id_" + field).select2({
        tags:true,
        tokenSeparators: [',' , " "],
        placeholder: "Search for " + field.toLocaleUpperCase(),
        minimumInputLength: 2,
        createSearchChoice:function(term, data) {
          if ($(data).filter(function() {
            return this.text.localeCompare(term)===0;
          }).length===0) {
            return {id:term, text:term};
          }
        },
        multiple: true,
        ajax: {

            url: request_url,
            dataType: 'json',
            data: function (term) {
                return {
                    query: term
                };
            },
            results: function (data) {
                var objects = [];
                $.each(data, function (i, obj) {
                    map[obj.name] = obj;
                    objects.push({
                        "text": obj.name,
                        'id': map[obj.name].id

                    });
                });
                return {results: objects};
            }
        },
        initSelection: function (element, callback) {
            var data_list = [];
            var promises = [];
            $(element.val().split(",")).each(function (index, id) {
                var that = this;
                promises.push($.get(request_url, {'id': id}).done(function (data) {
                    $.each(data, function (index, value) {
                        var result = value.name
                        data_list.push({id: that, text: result});
                    });
                }));
            });
            $.when.apply($, promises).done(function() {
                callback(data_list);
            });
        }
    })
}