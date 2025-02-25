import unittest

from pybbn.graph.potential import Potential, PotentialEntry


class TestPotential(unittest.TestCase):
    def setUp(self):
        """
        Setup.
        :return: None.
        """
        pass

    def tearDown(self):
        """
        Teardown.
        :return: None.
        """
        pass

    def test_potential_entry_matches(self):
        """
        Tests matching potential entry.
        :return: None.
        """
        entry1 = PotentialEntry()
        entry1.add(0, "on")
        entry1.add(1, "on")

        entry2 = PotentialEntry()
        entry2.add(0, "on")
        entry2.add(1, "on")

        entry3 = PotentialEntry()
        entry3.add(0, "on")
        entry3.add(1, "off")

        assert entry1.matches(entry2) == 1
        assert entry1.matches(entry3) == 0

    def test_potential_entry_duplicate(self):
        """
        Tests checking for potential duplicates.
        :return: None.
        """
        entry1 = PotentialEntry()
        entry1.add(0, "on")
        entry1.add(1, "on")

        entry2 = entry1.duplicate()

        assert entry1.matches(entry2) == 1

    def test_potential_get_matching_entry(self):
        """
        Tests get matching entry from potential.
        :return: None.
        """
        entry1 = PotentialEntry().add(0, "on").add(1, "on")
        entry2 = PotentialEntry().add(0, "on").add(1, "off")
        entry3 = PotentialEntry().add(0, "off").add(1, "on")
        entry4 = PotentialEntry().add(0, "off").add(1, "off")
        entry5 = PotentialEntry().add(3, "off").add(1, "off")

        potential = (
            Potential()
            .add_entry(entry1)
            .add_entry(entry2)
            .add_entry(entry3)
            .add_entry(entry4)
        )

        assert len(potential.get_matching_entries(entry1)) == 1
        assert len(potential.get_matching_entries(entry2)) == 1
        assert len(potential.get_matching_entries(entry3)) == 1
        assert len(potential.get_matching_entries(entry4)) == 1
        assert len(potential.get_matching_entries(entry5)) == 0

    def test_str(self):
        """
        Tests str function.
        :return: None.
        """
        entry1 = PotentialEntry().add(0, "on").add(1, "on")
        entry2 = PotentialEntry().add(0, "on").add(1, "off")
        entry3 = PotentialEntry().add(0, "off").add(1, "on")
        entry4 = PotentialEntry().add(0, "off").add(1, "off")

        potential = (
            Potential()
            .add_entry(entry1)
            .add_entry(entry2)
            .add_entry(entry3)
            .add_entry(entry4)
        )

        o = potential.__str__()
        e = "0=on,1=on|1.00000\n0=on,1=off|1.00000\n0=off,1=on|1.00000\n0=off,1=off|1.00000"
        assert o == e
