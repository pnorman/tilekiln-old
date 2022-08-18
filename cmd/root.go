/*
Copyright © 2022 Paul Norman <osm@paulnorman.ca>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/
package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

// rootCmd represents the base command when called without any subcommands
var (
	configFile string
	rootCmd    = &cobra.Command{
		Use:   "tilekiln",
		Short: "Tilekiln is a command-line utilities to generate and serve MVTs",
		Long: `Tilekiln is a command-line utilities to generate and serve
    Mapbox Vector Tiles (MVTs).

    Generation relies on the standard method of a PostgreSQL + PostGIS server as a
    data source, and ST_AsMVT to serialize the MVTs.

    The target use-case is vector tiles for OpenStreetMap Carto on
    openstreetmap.org, a worldwide complex basemap under high load.`,
	}
)

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVarP(&configFile, "config", "c", "", "Configuration file")
	rootCmd.MarkPersistentFlagRequired("config")
	rootCmd.MarkPersistentFlagFilename("config")
}
