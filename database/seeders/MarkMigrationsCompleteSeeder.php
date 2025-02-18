<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class MarkMigrationsCompleteSeeder extends Seeder
{
    /**
    * Run the database seeds.
    */
    public function run(): void
    {
        $migrations = [
            '0001_01_01_000001_create_cache_table',
            '0001_01_01_000002_create_jobs_table',
            '2024_01_29_163400_create_schemas',
            '2024_01_29_163500_create_reference_tables',
            '2024_01_29_163600_create_core_tables',
            '2024_01_29_163700_create_case_tables',
            '2024_02_02_163100_create_case_management_tables',
            '2024_02_02_194500_update_case_status_column',
        ];

        foreach ($migrations as $migration) {
            DB::table('migrations')->insert([
                'migration' => $migration,
                'batch' => 5
            ]);
        }
    }
}

