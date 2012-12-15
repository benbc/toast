(defproject toast "0.1.0-SNAPSHOT"
  :dependencies [[org.clojure/clojure "1.4.0"]
                 [compojure "1.1.3"]
                 [enlive "1.0.1"]]
  :plugins [[lein-ring "0.7.5"]]
  :ring {:handler toast.handler/app}
  :profiles
  {:dev {:dependencies [[ring-mock "0.1.3"]]}})
