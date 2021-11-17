class SequenceStatistics():
    """Provides layer sequence statistics.
    """

    def __init__(self, sequence, inference, hw_interactions, power_events):
        self._sequence = sequence
        self._inference = inference
        self._powers = {}
        if hw_interactions is not None:
            if power_events:

                def get_power_events(time_range):
                    result = []
                    for event in power_events:
                        if event.ts >= time_range[0] and event.ts <= time_range[
                                1]:
                            result.append(event)
                    return result

                # get power measure between program start & end
                self.powers['program'] = get_power_events(hw_interactions[:2])
                # get power mesures between inference start & end
                self.powers['inference'] = get_power_events(hw_interactions[2:])

    def __repr__(self):
        data = "{sequence: " + self._sequence.name
        fps = "N/A" if self.fps is None else "%.2f" % self.fps
        data += ", fps: " + fps
        if self._powers:
            data += ", powers: " + str(self._powers)
        return data

    def __str__(self):
        data = "Sequence " + self._sequence.name
        fps = "N/A" if self.fps is None else "%.2f" % self.fps + " fps"
        data += "\nAverage framerate = " + fps
        if self._powers and self._powers['inference']:

            def power(event):
                # voltage is in µV, current in mA, power is in mW.
                return event.voltage * event.current / 1000000

            # get all inference powers value
            all_powers = [power(event) for event in self.powers['inference']]
            # get avg/min/max
            avg_power = sum(all_powers) / len(all_powers)
            min_power = min(all_powers)
            max_power = max(all_powers)

            data += "\nLast inference power usage (mW): "
            data += f"Avg {avg_power:.2f} / Min {min_power:.2f} / Max {max_power:.2f}"
        return data

    @property
    def fps(self):
        if self._inference is not None:
            return 1000 * self._inference[0] / self._inference[1]
        return None

    @property
    def powers(self):
        return self._powers


def _get_metrics(model, sequence, metrics):
    """Return the metrics for a specific sequence
    """
    if len(model.metrics.names) == 0:
        return None
    # Sequence metrics are identified by the first and last layers
    prefix = sequence.name
    # Filter-out metrics not corresponding to that sequence
    seq_metrics_names = [name for name in model.metrics.names if prefix in name]
    # Get the metrics matching the specified name for the sequence
    metrics_names = [name for name in seq_metrics_names if metrics in name]
    if len(metrics_names) > 0:
        return model.metrics[metrics_names[0]]
    return None


class Statistics:
    """Provides statistics for all Model layer sequences.
    """

    def __init__(self, model):
        self._stats = {}
        # Iterate through model layer sequences
        for sequence in model.sequences:
            # Get metrics for the sequence
            inference = _get_metrics(model, sequence, "inference")
            hw_interactions = _get_metrics(model, sequence,
                                           "hardware_interactions")
            self._stats[sequence.name] = SequenceStatistics(
                sequence, inference, hw_interactions, model.power_events)

    def __str__(self):
        data = ""
        for _, stat in self._stats.items():
            if stat.fps is not None:
                data += "\n" + stat.__str__()
        if not data:
            data = "N/A"
        return data

    def __repr__(self):
        return self._stats.__repr__()

    def __getitem__(self, key):
        # Look first for a Sequence statistics
        if key in self._stats:
            return self._stats[key]
        raise KeyError

    def __len__(self):
        return len(self._stats)

    def __iter__(self):
        return iter(self._stats.items())

    def keys(self):
        return self._stats.keys()

    def items(self):
        return self._stats.items()
