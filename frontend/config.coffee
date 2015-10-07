exports.config =
  paths:
    public: '../app/static/'
  files:
    javascripts:
      joinTo:
        '../../app/static/javascripts/app.js': /^app/
        '../../app/static/javascripts/vendor.js': /^(?!app)/
      order:
        before: [
          'bower_components/jquery/dist/jquery.js'
        ]
        after: [
          'vendor/jquery.bootstrap.patch.js'
        ]

    stylesheets:
      joinTo: '../../app/static/stylesheets/style.css'
      order:
        after: ['bower_components/jquery-ui/themes/overcast/jquery-ui.css']

  sourceMaps: false
